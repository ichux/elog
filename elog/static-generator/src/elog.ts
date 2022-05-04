import Alpine from "alpinejs";
import Notification from "./alert";
import {Grid, html} from "gridjs";
import {RowSelection} from "gridjs/plugins/selection";
import {LogRecord, LogRecordTuple} from "./types";
import {parse} from "json2csv";
import "./gridjs.css";

const elog = () => ({
  options: {contentLength: 20},
  data: [] as Array<LogRecordTuple>,
  csrf: "",
  grid: undefined as Grid | undefined,
  innerModalHeight: "auto" as number | "auto",
  searchQuery: '',
  showAvailableOptionsView: false,
  showRecordDetailsView: false,
  currentSelection: [] as [string, any][],
  currentSelectionId: '',
  checkAll() {
    document
      .querySelectorAll("input.gridjs-checkbox")
      .forEach((element: Element) => {
        const checked = (element as HTMLInputElement).checked;
        if (!checked) {
          (element as HTMLElement).click();
        }
      });
  },
  uncheckAll() {
    document
      .querySelectorAll("input.gridjs-checkbox")
      .forEach((element: Element) => {
        const checked = (element as HTMLInputElement).checked;
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
  extractData([
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
  ]: LogRecordTuple): object {
    return {
      Id: id,
      Code: (code as any).val, // Attached as custom property as code is a VNode
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
    };
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
        Notification.warn.fire({text: 'Nothing to copy'});
        return;
      }

      let records = this.data.filter((record: LogRecordTuple) =>
        rowIds.includes(record[0])
      );
      const extracted = records.map(this.extractData);
      const csv = parse(extracted, {fields, eol: "\n"});
      await navigator.clipboard.writeText(csv);
      Notification.success.fire({text: `${extracted.length} records copied`});
    } catch (e) {
      Notification.alert.fire({text: 'An error occured :('});
    }
  },
  async deleteSelection() {
    const rowIds = this.getSelectedRowIds();

    if (rowIds.length == 0) {
      Notification.warn.fire({text: "Nothing to delete"});
      return;
    }

    const response = await fetch("/elog-delete", {
      method: "POST",
      headers: {
        "X-CSRFToken": this.csrf,
        "Content-Type": "application/json;charset=UTF-8",
      },
      body: JSON.stringify({ids: rowIds}),
    });

    if (response.ok) {
      this.grid?.forceRender();
    }
  },
  showDetails(...args: any[]): void {
    const {currentTarget} = args[0];
    let data = decodeURIComponent(currentTarget.querySelector('td[data-column-id="code"] div[data-record]')?.getAttribute('data-record'));
    data = JSON.parse(data);
    const {_id} = args[1];
    if (this.currentSelectionId === _id) {
      return;
    }
    this.currentSelectionId = _id;
    this.currentSelection = [
      ["Id", data[0]],
      ["HTTP Method", data[2]],
      ["Code", data[1]],
      ["Error type", data[5]],
      ["Error message", data[3]],
      ["Error traceback", data[4]],
      ["Referrer", data[8]],
      ["Post values", data[7]],
      ["Request args", data[9]],
      ["Request path", data[10]],
      ["Ip", data[6]],
      ["User Agent", data[11]],
      ["User browser", data[12]],
      ["User browser version", data[13]],
      ["User platform", data[14]],
      ["When", data[15]],
    ];
    this.showRecordDetailsView = true;
  },
  onGridReady() {
    this.innerModalHeight =
      document.querySelector(".gridjs.gridjs-container")?.getBoundingClientRect().height ??
      "auto";

    // This attempt to prevent checkboxes click
    // events to hit row and trigger undesired actions
    document
      .querySelectorAll("input.gridjs-checkbox")
      .forEach((element: Element) => {
        element.addEventListener("click", (e) => e.stopPropagation());
      });

    this.grid?.on("rowClick", this.showDetails.bind(this));
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
      const {data, recordsTotal} =
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
        }: LogRecord) => {
          const initialData: any[] = [
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

          // The goal is to save the whole data as an attribute for later access
          // See https://stackoverflow.com/questions/8542746/store-json-object-in-data-attribute-in-html-jquery
          // for why encodeURIComponent.
          initialData[1] = html(`<div data-record="${encodeURIComponent(JSON.stringify(initialData))}">${code}</div>`, 'div')
          initialData[1].val = code;
          return initialData;
        });
      this.data = transformedData;
      return {data: transformedData, total: recordsTotal};
    } else {
      throw Error("Data retrieving error");
    }
  },
  init(): void {
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
        {name: "Id", hidden: true},
        {name: "Code", },
        {name: "HTTP Method"},
        {name: "Error message", hidden: true},
        {name: "Error traceback", hidden: true},
        {name: "Error type"},
        {name: "Ip"},
        {name: "Post values"},
        {name: "Referrer"},
        {name: "Request args"},
        {name: "Request path"},
        {name: "User Agent"},
        {name: "User browser"},
        {name: "User browser version"},
        {name: "User platform"},
        {name: "When"},
      ],
      // data: this.loadData.bind(this),
      server: {
        url: "/data",
        data: this.loadData.bind(this),
      },
      pagination: {
        enabled: true,
        limit: this.options.contentLength,
        server: {
          url: this.buildURL.bind(this),
        },
      },
    });
    this.grid.on("ready", this.onGridReady.bind(this));
    this.grid.render((this as any).$refs["tableWrapper"]);
  },
  /////// Helpers
  getSelectedRowIds() {
    const checkboxPlugin = this.grid?.config.plugin.get("checkboxes");
    // Returned object is normally a proxy so we get the target
    const {rowIds}: {rowIds: (string | number)[]} = JSON.parse(
      JSON.stringify(checkboxPlugin?.props?.store.state)
    );
    return rowIds;
  },
  formatHtml(record: [string, unknown]) {
    switch (record[0]) {
      case "Error message":
      case "Error traceback":
      case "Error type":
        return (record[1] as any).replaceAll(/<br\/?>/g, "\n");
      default:
        return new Option(record[1] as any).innerHTML;
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
  isCode(field: string): boolean {
    return ["Error message", "Error traceback", "Error type"].includes(
      field as never
    );
  },
  updatePaginationConfig(value: number) {
    this.uncheckAll();
    this.options.contentLength = value;
    this.grid?.updateConfig({
      pagination: {
        enabled: true,
        limit: value,
      },
    })
      .forceRender();
  },
  updateTable() {
    this.uncheckAll();
    this.grid?.forceRender();
  },
  buildURL(prevUrl: string, page: number, limit: number) {
    const searchParams = this.searchQuery.length > 0 ? `&search[value]=${this.searchQuery}` : "&search[value]=date:today"
    // Remove old query params before doing the stuff
    return `${prevUrl.replace(/\?.*$/, "")}?length=${limit}&start=${page * limit
      }${searchParams}`;
  }
});

Alpine.data("elog", elog);
document.addEventListener("DOMContentLoaded", Alpine.start);
