from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Template for Python-driven OriginPro plotting with originpro."
    )
    parser.add_argument("data_file", type=Path, help="Input Excel or CSV file.")
    parser.add_argument("--sheet", default=0, help="Excel sheet name or index.")
    parser.add_argument("--out", type=Path, default=Path("plots_origin"), help="Output folder.")
    parser.add_argument("--tmp", type=Path, default=Path("E:/origin_tmp"), help="ASCII temp folder.")
    parser.add_argument("--show", action="store_true", help="Show Origin while plotting.")
    return parser.parse_args()


def read_table(path: Path, sheet: str | int) -> pd.DataFrame:
    if path.suffix.lower() in {".xlsx", ".xls", ".xlsm"}:
        return pd.read_excel(path, sheet_name=sheet)
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    raise ValueError(f"Unsupported input file type: {path.suffix}")


def prepare_data(raw: pd.DataFrame) -> pd.DataFrame:
    """Replace this function with project-specific cleanup and sorting."""
    df = raw.copy()
    df = df.dropna(how="all").reset_index(drop=True)
    if "Label" not in df.columns:
        df.insert(0, "Label", [f"P{i + 1}" for i in range(len(df))])
    return df


def export_graph(graph, filename: str, out_dir: Path, tmp_dir: Path) -> Path:
    tmp_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)
    tmp_file = tmp_dir / filename
    final_file = out_dir / filename
    saved = graph.save_fig(str(tmp_file), type=Path(filename).suffix.lstrip(".") or "png", width=1800)
    if saved:
        shutil.copy2(tmp_file, final_file)
    return final_file


def save_project(op, out_dir: Path, tmp_dir: Path, project_name: str) -> Path:
    tmp_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    tmp_opju = tmp_dir / f"{project_name}_{stamp}.opju"
    final_opju = out_dir / f"{project_name}.opju"
    op.save(str(tmp_opju))
    if tmp_opju.exists():
        try:
            shutil.copy2(tmp_opju, final_opju)
        except PermissionError:
            final_opju = out_dir / f"{project_name}_{stamp}.opju"
            shutil.copy2(tmp_opju, final_opju)
    return final_opju


def build_origin_project(df: pd.DataFrame, out_dir: Path, tmp_dir: Path, show: bool) -> None:
    import originpro as op

    op.set_show(show)
    op.new()
    try:
        wb = op.new_book(lname="Origin_Input_Data")
        wks = wb[0]
        wks.from_df(df)

        # Adapt column designations after choosing X/Y columns.
        # Example for Label + numeric Y columns: one X followed by N Y columns.
        if len(df.columns) > 1:
            wks.cols_axis("x" + "y" * (len(df.columns) - 1), c1=0, repeat=False)

        gp = op.new_graph(lname="Origin_Example_Column_Plot")
        gl = gp[0]
        if len(df.columns) < 2:
            raise ValueError("Need at least one X/label column and one Y column to plot.")
        plot = gl.add_plot(wks, colx=0, coly=1, type="c")
        plot.color = "#4E6E8E"
        gl.axis("x").title = str(df.columns[0])
        gl.axis("y").title = str(df.columns[1])
        gl.rescale()
        gl.lt_exec(
            "layer.grid.majorY.show=1; "
            "layer.grid.majorY.color=15; "
            "layer.grid.majorY.lineStyle=2; "
            "layer.x.label.rotate=45;"
        )
        gp.lt_exec("legend -r;")

        export_graph(gp, "Origin_Example_Column_Plot.png", out_dir, tmp_dir)
        save_project(op, out_dir, tmp_dir, "origin_python_plot")
    finally:
        op.exit()


def main() -> None:
    args = parse_args()
    out_dir = args.out.resolve()
    tmp_dir = args.tmp.resolve()
    raw = read_table(args.data_file.resolve(), args.sheet)
    df = prepare_data(raw)
    out_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_dir / "origin_input_data_sorted.csv", index=False, encoding="utf-8-sig")
    build_origin_project(df, out_dir, tmp_dir, args.show)
    print(f"Wrote Origin outputs to: {out_dir}")


if __name__ == "__main__":
    main()
