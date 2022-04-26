import Alpine from "alpinejs";
import { Grid } from "gridjs";
import { RowSelection } from "gridjs/plugins/selection";
import { LogRecord, LogRecordTuple } from "./types";
import { parse } from "json2csv";
import "./gridjs.css";

Alpine.data("elog", () => ({
  data: [] as Array<LogRecordTuple>,
  csrf: "",
  grid: undefined as Grid | undefined,
  async showAvailableOptions() {},
  async copySelectionAsCSV() {
    try {
      const fields = [
        "Id",
        "Code",
        "HTTP Method",
        "Error message",
        "Error traceback",
        "Error type",
        "Ip",
        "Post values",
        "Referrer",
        "Request args",
        "Request path",
        "User Agent",
        "User browser",
        "User browser version",
        "User platform",
        "When",
      ];
      const rowIds = this.getSelectedRowIds();

      if (rowIds.length == 0) {
        alert("Nothing to copy! TODO: Modals");
        return;
      }

      let records = this.data.filter((record: LogRecordTuple) =>
        rowIds.includes(record[0])
      );
      records = records.map(
        ([
          id,
          code,
          httpmethod,
          errormsg,
          errortraceback,
          errortype,
          ip,
          postvalues,
          referrer,
          requestargs,
          requestpath,
          useragent,
          userbrowser,
          userbrowserversion,
          userplatform,
          when,
        ]: LogRecordTuple): object => ({
          Id: id,
          Code: code,
          "HTTP Method": httpmethod,
          "Error message": errormsg,
          "Error traceback": errortraceback,
          "Error type": errortype,
          Ip: ip,
          "Post values": postvalues,
          Referrer: referrer,
          "Request args": requestargs,
          "Request path": requestpath,
          "User Agent": useragent,
          "User browser": userbrowser,
          "User browser version": userbrowserversion,
          "User platform": userplatform,
          When: when,
        })
      );
      const csv = parse(records, { fields, eol: "\n" });
      await navigator.clipboard.writeText(csv);
      alert("Copied! TODO: Use modals");
    } catch (e) {
      console.log(e);
    }
  },
  async deleteSelection() {
    const rowIds = this.getSelectedRowIds();

    if (rowIds.length == 0) {
      alert("Nothing to delete! TODO: Modals");
      return;
    }

    const response = await fetch("/elog-delete", {
      method: "POST",
      headers: {
        "X-CSRFToken": this.csrf,
        "Content-Type": "application/json;charset=UTF-8",
      },
      body: JSON.stringify({ ids: rowIds }),
    });

    if (response.ok) {
      console.log(await response.json());
      // Update the table then
      // This is a temporary solution as it will
      // probably conflict with server side configurations
      this.grid
        .updateConfig({
          data: this.data.filter((r: LogRecordTuple) => !rowIds.includes(r[0])),
        })
        .forceRender();
    }
  },
  onGridReady() {},
  initCsrf() {
    const meta: HTMLMetaElement | null = document.querySelector(
      "meta[name='csrf-token']"
    );
    this.csrf = meta?.content ?? "";
  },
  async loadData() {
    const response = await fetch("/data", {
      headers: {
        "X-CSRFToken": this.csrf,
        "Content-Type": "application/json;charset=UTF-8",
      },
    });
    if (response.ok) {
      const { data /** recordsFiltered, recordsTotal **/ } =
        await response.json();
      const transformedData = data.map(
        ({
          id,
          code,
          httpmethod,
          errormsg,
          errortraceback,
          errortype,
          ip,
          postvalues,
          referrer,
          requestargs,
          requestpath,
          useragent,
          userbrowser,
          userbrowserversion,
          userplatform,
          when,
        }: LogRecord) => [
          id,
          code,
          httpmethod,
          errormsg,
          errortraceback,
          errortype,
          ip,
          postvalues,
          referrer,
          requestargs,
          requestpath,
          useragent,
          userbrowser,
          userbrowserversion,
          userplatform,
          when,
        ]
      );
      this.data = transformedData;
      return transformedData;
    } else {
      throw Error("Data retrieving error");
    }
  },
  async init(): Promise<void> {
    this.initCsrf();
    this.grid = new Grid({
      columns: [
        {
          id: "checkboxes",
          name: "#",
          sort: false,
          plugin: {
            component: RowSelection,
            props: {
              id: (row: any) => row.cell(1).data,
            },
          },
        },
        { name: "Id", hidden: true },
        "Code",
        "HTTP Method",
        { name: "Error message", hidden: true },
        { name: "Error traceback", hidden: true },
        "Error type",
        "Ip",
        "Post values",
        "Referrer",
        "Request args",
        "Request path",
        "User Agent",
        "User browser",
        "User browser version",
        "User platform",
        "When",
      ],
      data: this.loadData.bind(this),
      pagination: {
        enabled: true,
        limit: 20,
        summary: false,
      },
    });
    this.grid.on("ready", this.onGridReady.bind(this));
    this.grid.render(this.$refs["tableWrapper"]);
  },
  /////// Helpers
  getSelectedRowIds() {
    const checkboxPlugin = this.grid.config.plugin.get("checkboxes");
    // Returned object is normally a proxy so we get the target
    const { rowIds }: { rowIds: (string | number)[] } = JSON.parse(
      JSON.stringify(checkboxPlugin.props.store.state)
    );
    return rowIds;
  },
}));

document.addEventListener("DOMContentLoaded", Alpine.start);
