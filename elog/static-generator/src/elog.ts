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
  showAvailableOptionsView: false,
  showRecordDetailsView: false,
  currentSelection: [] as [string, any][], // tuple
  checkAll() {
    document
      .querySelectorAll("input.gridjs-checkbox")
      .forEach((element: Element) => {
        const checked = (element as HTMLInputElement).checked == true;
        if (!checked) {
          (element as HTMLElement).click();
        }
      });
  },
  uncheckAll() {
    document
      .querySelectorAll("input.gridjs-checkbox")
      .forEach((element: Element) => {
        const checked = (element as HTMLInputElement).checked == true;
        if (checked) {
          (element as HTMLElement).click();
        }
      });
  },
  toggleSelection() {
    document
      .querySelectorAll("input.gridjs-checkbox")
      .forEach((element: Element) => {
        (element as HTMLElement).click();
      });
  },
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
      this.grid.forceRender();
    }
  },
  async showDetails(...args: any[]) {
    const { _cells: cells } = args[1]; // Retrive record fields
    cells.shift(); // Remove the first column as it's for the checkbox
    this.currentSelection = [
      ["Id", cells[0]?.data],
      ["HTTP Method", cells[2]?.data],
      ["Code", cells[1]?.data],
      ["Error type", cells[5]?.data],
      ["Error message", cells[3]?.data],
      ["Error traceback", cells[4]?.data],
      ["Referrer", cells[8]?.data],
      ["Post values", cells[7]?.data],
      ["Request args", cells[9]?.data],
      ["Request path", cells[10]?.data],
      ["Ip", cells[6]?.data],
      ["User Agent", cells[11]?.data],
      ["User browser", cells[12]?.data],
      ["User browser version", cells[13]?.data],
      ["User platform", cells[14]?.data],
      ["When", cells[15]?.data],
    ];
    this.showRecordDetailsView = true;
  },
  onGridReady() {
    // This attempt to prevent checkboxes click
    // events to hit row and trigger undesired actions
    document
      .querySelectorAll("input.gridjs-checkbox")
      .forEach((element: Element) => {
        element.addEventListener("click", (e) => e.stopPropagation());
      });
    this.grid.on("rowClick", this.showDetails.bind(this));
  },
  initCsrf() {
    const meta: HTMLMetaElement | null = document.querySelector(
      "meta[name='csrf-token']"
    );
    this.csrf = meta?.content ?? "";
  },
  async loadData(options: any) {
    const response = await fetch(options.url, {
      headers: {
        "X-CSRFToken": this.csrf,
        "Content-Type": "application/json;charset=UTF-8",
      },
    });
    if (response.ok) {
      const { data /** recordsFiltered **/, recordsTotal } =
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
      return { data: transformedData, total: recordsTotal };
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
      // data: this.loadData.bind(this),
      server: {
        url: "/data",
        data: this.loadData.bind(this),
      },
      pagination: {
        enabled: true,
        limit: 20,
        server: {
          url: (prevUrl: string, page: number, limit: number) => {
            // Remove old query params before doing the stuff
            return `${prevUrl.replace(/\?.*$/, "")}?length=${limit}&start=${
              page * limit
            }`;
          },
        },
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
  formatHtml(record: [string, any]) {
    switch (record[0]) {
      case "Error message":
      case "Error traceback":
      case "Error type":
        return `<pre class="py-2"><code>${
          new Option(record[1].replaceAll(/<br\/?>/g, "\n")).innerHTML
        }</pre></code>`;
      default:
        return new Option(record[1]).innerHTML;
    }
  },
  async copyToClipboard(text: string): Promise<boolean> {
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch {
      return false;
    }
  },
}));

document.addEventListener("DOMContentLoaded", Alpine.start);
