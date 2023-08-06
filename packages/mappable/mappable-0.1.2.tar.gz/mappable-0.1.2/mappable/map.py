from typing import List, Dict, Union
import os
import math
import datetime
from collections import Counter

import sqlite_utils
import pandas
import numpy
from pydantic import BaseModel

DEFAULT_MAPPABLE_DIR = "~/.mappable"


class Label(BaseModel):
    name: str
    light: str
    dark: str


def create_initial_label_colours(labels: List[str]) -> List[Label]:

    num_labels = len(labels)
    hues = [math.floor((255 / num_labels) * i) for i in range(num_labels)]

    coloured_labels = [
        Label(
            name=label,
            light=f"hsla({hue}, 80%, 50%, 0.4)",
            dark=f"hsla({hue}, 100%, 50%, 0.8)",
        )
        for (label, hue) in zip(labels, hues)
    ]
    return coloured_labels


NONE_LABEL = Label(
    name="None",
    light="hsla(215, 40%, 50%, 0.40)",
    dark="hsla(215, 60%, 50%, 0.8)",
)


def get_empty_info(name: str, description: str, created_at: str):
    return {
        "name": name,
        "description": description,
        "created_at": created_at,
        "label_count": 0,
        "labeled_percent": 0,
        "count": 0,
        "label_statistics": [],
        "columns": [],
        "types": [],
        "label_column": "label",
        "default_view_id": None,
        "searchable": False,
    }


class MappableDataset:
    def __init__(
        self, name: str, description: str = "", directory: str = DEFAULT_MAPPABLE_DIR
    ):

        self._root_dir = os.path.expanduser(directory)
        os.makedirs(self._root_dir, exist_ok=True)
        db_path = os.path.join(self._root_dir, name + ".db")
        exists = os.path.exists(db_path)
        self.db = sqlite_utils.Database(db_path)
        self.name = name

        if not exists:
            # Record some info about the creation of the dataset.
            now = datetime.datetime.now().strftime("%m/%d/%Y at %I:%M%p")
            self.db["admin"].insert_all(
                [
                    {"key": "name", "value": name},
                    {"key": "description", "value": description},
                    {"key": "created_at", "value": now},
                ],
                pk="key",
            )

    def info(self):

        description = self.db["admin"].get("description")["value"]
        created_at = self.db["admin"].get("created_at")["value"]

        if not self.db["data"].exists():
            return get_empty_info(self.name, description, created_at)

        # Set the limit really high here, so we get all the stats in one blob,
        # rather than split betwen the most_common/least_common attributes.
        label_info = self.db["data"].analyze_column("label", common_limit=100_000)

        # Find the None label:

        label_stats = []
        none_count = 0
        for (label, count) in label_info.most_common:

            blob = {"name": label, "count": count}
            label_stats.append(blob)
            if label == NONE_LABEL.name:
                none_count = count

        percentage_labelled = round(1 - (none_count / label_info.total_rows), 2) * 100
        points_tables = [
            x.name.replace("points_", "")
            for x in self.db.tables
            if x.name.startswith("points_")
        ]

        default_view_id = None
        if points_tables:
            default_view_id = points_tables[0]

        return {
            "name": self.name,
            "description": description,
            "created_at": created_at,
            "label_count": label_info.num_distinct,
            "labeled_percent": percentage_labelled,
            "count": label_info.total_rows,
            "label_statistics": [
                {"name": name, "count": count}
                for (name, count) in label_info.most_common
            ],
            "columns": [x.name for x in self.db["data"].columns],
            "types": [x.type for x in self.db["data"].columns],
            "label_column": "label",
            "default_view_id": default_view_id,
            "searchable": self.searchable(),
        }

    def add_description(self, description: str) -> None:
        self.db["admin"].upsert(
            {"name": "description", "value": description}, pk="name"
        )

    def add_json(
        self,
        data: List[Dict[str, any]],
        label_column: str = None,
        searchable: bool = True,
        search_columns: List[str] = None,
    ):
        self.add_pandas(
            pandas.DataFrame(data),
            label_column=label_column,
            searchable=searchable,
            search_columns=search_columns,
        )


    def add_column(self, name: str, column_data) -> None:

        # +1 because sqlite is 1-indexed.
        records = ({"rowid": i + 1, name: x} for i, x in enumerate(column_data))
        types = sqlite_utils.db.suggest_column_types([{name: column_data[0]}])

        self.db["data"].add_column(name, types[name])
        self.db["data"].upsert_all(records, pk="rowid")

    def add_pandas(
        self,
        data: pandas.DataFrame,
        label_column: str = None,
        searchable: bool = True,
        search_columns: List[str] = None,
    ):

        has_data = self.db["data"].exists() and self.db["data"].count > 0
        if has_data:
            raise ValueError(
                f" {self.name} already has data. Adding data to existing datasets is not supported yet!"
            )

        # Lowercase dataframe names, because sqlite is case insensitve.
        if label_column is not None:
            label_column = label_column.lower()
        if search_columns:
            search_columns = [x.lower() for x in search_columns]

        lowercase_names = [x.lower() for x in data.columns]
        if len(set(lowercase_names)) != len(lowercase_names):
            raise ValueError(
                "Mappable stores data in sqlite, which has case insensitive columns. The dataframe passed in has case sensitive columns (i.e 'A' and 'a')"
            )

        if not all(lowercase_names == data.columns):
            print("Warning - Sqlite is not case sensitive. Converting column names to lowercase.")

        data.columns = lowercase_names
        populated_labels = "label" in lowercase_names or label_column is not None

        def none_or_existing_label(record):
            if label_column is not None:
                return record[label_column]

            if "label" in data.columns:
                return record["label"]
            else:
                return NONE_LABEL.name

        self.db["data"].insert_all(
            (
                {**record, **{"label": none_or_existing_label(record)}}
                for record in data.to_dict("records")
            )
        )

        if populated_labels:
            col = label_column or "label"
            labels = list(data[col].unique())
            self.add_labels(labels)
        # Add a None label.
        self.add_label(NONE_LABEL.dict())

        if searchable:
            if search_columns is None:
                search_columns = [
                    col.name for col in self.db["data"].columns if col.type == "TEXT"
                ]
            if not search_columns:
                raise ValueError(
                    "To make a dataset searchable, there must be text valued columns. If your data is not searchable, pass `searchable=False` to Dataset.add()"
                )
            self.db["data"].enable_fts(columns=search_columns)

    def to_json(self):
        return [blob for blob in self.db["data"].rows]

    def to_pandas(self):
        return pandas.DataFrame(self.db["data"].rows)

    def searchable(self):
        return self.db["data"].exists() and self.db["data"].detect_fts()

    def add_labels(self, labels):

        if isinstance(labels[0], str):
            labels = create_initial_label_colours(labels)
            labels = [x.dict() for x in labels]

        self.db["labels"].insert_all(labels, pk="name")

    def add_label(self, label):
        self.add_labels([label])

    def delete_label(self, label):
        to_update = (
            {"rowid": x, "label": NONE_LABEL.name}
            for x, y in self.db["data"].pks_and_rows_where(f"label = ?", [label])
        )
        self.db["data"].upsert_all(to_update, pk="rowid")
        self.db["labels"].delete(label)

    def count_labels(self, label: str):
        return self.db["data"].count_where("label = ?", [label])

    def get_labels(self):
        return list(self.db["labels"].rows)

    def add_points(self, name: str, points: Union[List[List[float]], numpy.ndarray]):

        if self.db[f"points_{name}"].exists():
            raise ValueError(f"{name} already exists as a view on {self.name} dataset.")

        if isinstance(points, numpy.ndarray):
            points = points.tolist()

        points_length = len(points)
        data_length = self.db["data"].count

        if points_length != data_length:
            raise ValueError(
                f"The number of points added ({points_length}) must equal the number of datapoints ({data_length})."
            )

        dim = len(points[0])
        if dim not in {2, 3}:
            raise ValueError(
                f"Mappable only supports 2D or 3D datapoints, but found {dim} dim points."
            )

        if dim == 2:
            it = ({"x": x, "y": y} for x, y in points)
        else:
            it = ({"x": x, "y": y, "z": z} for x, y, z in points)
        self.db[f"points_{name}"].insert_all(it)

    def get_points(self, name: str):

        table = self.db[f"points_{name}"]
        if not table.exists():
            raise ValueError(
                f"That points view ({name}) doesn't exist. Did you mean one of:{self.views()}"
            )

        if len(table.columns) == 3:
            raw_points = [[x["x"], x["y"], x["z"]] for x in table.rows]
        else:
            raw_points = [[x["x"], x["y"]] for x in table.rows]

        raw_metadata = list(self.db["data"].rows)
        return {"points": raw_points, "metadata": raw_metadata}

    def views(self) -> List[str]:
        table_names = [x.name for x in self.db.tables]

        return [
            x.replace("points_", "") for x in table_names if x.startswith("points_")
        ]

    def neighbors(self) -> List[str]:
        table_names = [x.name for x in self.db.tables]
        return [
            x.replace("neighbors_", "") for x in table_names if x.startswith("neighbors_")
        ]

    def add_neighbors(self, name: str, neighbors):

        if self.db[f"neighbors_{name}"].exists():
            raise ValueError(
                f"{name} already exists as a set of neighbors for the {self.name} dataset."
            )

        if isinstance(neighbors, numpy.ndarray):
            neighbors = neighbors.tolist()

        neighbors_length = len(neighbors)
        data_length = self.db["data"].count

        if neighbors_length != data_length:
            raise ValueError(
                f"The number of neighbors added ({neighbors_length}) must equal the number of datapoints ({data_length})."
            )

        blobs = []
        for i, row in enumerate(neighbors):
            for k, n in enumerate(row):
                blobs.append({"idx": i, "neighbor": int(n), "k": k})

        self.db[f"neighbors_{name}"].insert_all(blobs)

    def add_annotations(self, points: List[int], label: str):
        self.db["data"].upsert_all(
            ({"rowid": x + 1, "label": label} for x in points), pk="rowid"
        )

    def add_umap(self, name: str, umap: "umap.UMAP"):

        # HACK: This fixes the problem of umap having disconected vertices
        # by setting all the coordinates of the disconected vertices to 0.0,
        # which is almost certainly undesirable. In the future these points should
        # be removed and shown to the user seperately.
        points = numpy.nan_to_num(umap.embedding_).tolist()
        self.add_points(name, points)
        self.add_neighbors(name, umap._knn_indices)

    def recommend(
        self,
        view_id: str,
        points: List[int],
        minSimilarity: float,
        percent: int,
        includeLabelled: bool,
        excludedPoints: List[int],
    ) -> List[int]:

        if not self.db[f"neighbors_{view_id}"].exists():
            neighbors = self.neighbors()
            # Dataset has no views, we can't provide any recommendations.
            if not neighbors:
                return []
            else:
                # Choose the first one as a default.
                view_id = neighbors[0]

        dataset_k = self.db.execute(
            f"select max(k) from neighbors_{view_id}"
        ).fetchone()[0]

        top_k = int(dataset_k * (1 - minSimilarity))
        string_points = [str(x) for x in points]
        recommended = self.db[f"neighbors_{view_id}"].rows_where(
            f"k < {top_k} and idx in ({','.join(string_points)})"
        )

        excluded = set(excludedPoints)
        non_labelled_points = {
            # -1 because sqlite row index is 1 indexed.
            x - 1
            for x, y in self.db["data"].pks_and_rows_where(
                f"label = '{NONE_LABEL.name}' "
            )
        }

        count = Counter()
        selected_points = set(points)
        for point in recommended:
            neighbor = point["neighbor"]

            # # TODO this should be in the initial sql query, really.
            # We only want neighbors which are:

            # ...valid
            if neighbor < 0:
                # sometimes the NN is -1, I think maybe when the point is disconnected?
                continue

            # ...unlabelled, if the user requested only unlabelled points.
            if not includeLabelled and neighbor not in non_labelled_points:
                continue

            # ...not explicitly excluded
            if neighbor in excluded:
                continue

            # ...and not currently selected.
            if neighbor in selected_points:
                continue

            count[neighbor] += 1

        # Now filter to only those neighbors who are similar to at least "percent" percent
        # of the points in the selection.
        num_points = len(selected_points)
        recommended_points = []
        for p, c in count.most_common():
            if c / num_points * 100 >= percent:
                recommended_points.append(p)
        return recommended_points

    def search(self, q: str) -> List[int]:

        if self.db["data"].detect_fts() is None:
            # TODO throw an error here and surface in UI if FTS is not enabled.
            return []
        results = [x for x in self.db["data"].search(q, columns=["rowid"])]
        # sqlite is 1-indexed - so we convert the indices back to zero indexed.
        return [x["rowid"] - 1 for x in results]

    def __len__(self):
        if self.db["data"].exists():
            return self.db["data"].count
        else:
            return 0

    def __getitem__(self, val):
        size = self.db["data"].count

        def handle_index(n):
            if n > size:
                raise IndexError(
                    f"Invalid index for dataset {self.name} of size: {size}"
                )
            if n >= 0:
                return n
            else:
                return n + size

        if isinstance(val, slice):
            start = handle_index(val.start or 0)
            end = handle_index(val.stop or size)
            indices = range(start, end, val.step or 1)
            # +1 because sqlite row indices are 1 indexed.
            return [self.db["data"].get(i + 1) for i in indices]

        elif isinstance(val, int):
            index = handle_index(val)
            # +1 because sqlite row indices are 1 indexed.
            return self.db["data"].get(index + 1)
        else:
            raise ValueError("Index must be an int or a slice, like data[1:2].")


class Mappable:
    def __init__(self, directory: str = DEFAULT_MAPPABLE_DIR):

        self._root_dir = os.path.expanduser(directory)
        os.makedirs(self._root_dir, exist_ok=True)

        names = [x[:-3] for x in os.listdir(self._root_dir) if x.endswith(".db")]

        self.names = names

    def datasets(self) -> List[str]:
        return self.names

    # In these two methods, it might seem a bit odd to recreate the MappableDataset
    # each time. But this is important, because the server is async, and sqlite connections
    # can't be shared across threads, so we need to be able to create a db connection
    # in the same thread as the request.

    def info(self):
        descriptions = []
        for name in self.names:
            description = self.get(name).info()
            descriptions.append(description)

        return descriptions

    def get(self, name: str) -> MappableDataset:
        if name not in self.names:
            raise ValueError(
                f"That dataset doesn't exist. You can create it with Mappable.new('{name}'')"
            )

        return MappableDataset(name, directory=self._root_dir)

    def new(self, name: str) -> MappableDataset:

        if name in self.names:
            raise ValueError("That dataset already exists!")

        self.names.append(name)

        return MappableDataset(name, directory=self._root_dir)
