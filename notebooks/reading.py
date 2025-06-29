import marimo

__generated_with = "0.14.9"
app = marimo.App(width="medium")


@app.cell
def _():
    from pyiceberg.catalog import load_catalog
    import pyarrow as pa
    import pyarrow.dataset as ds
    import pyarrow.fs as fs


    catalog = load_catalog("default")
    return (catalog,)


@app.cell
def _(catalog):
    catalog.list_namespaces()
    return


@app.cell
def _(catalog):
    catalog.list_tables(namespace="nyc")
    return


@app.cell
def _(catalog):
    fhvhv = catalog.load_table(("nyc.fhvhv"))
    return (fhvhv,)


@app.cell
def _(fhvhv):
    fhvhv.scan(limit=100).to_arrow()
    return


if __name__ == "__main__":
    app.run()
