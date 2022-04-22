import Alpine from "alpinejs";
import { Grid } from "gridjs";
import { RowSelection } from "gridjs/plugins/selection";
import fakeData from "./faker";
import "./gridjs.css";

Alpine.data("elog", () => ({
  csrf: "",
  grid: undefined as Grid | undefined,
  updateSelectionState(state: any, previousState: any) {
    console.log("Update: ", state, previousState);
  },
  onGridReady() {
    const checkboxPlugin = this.grid.config.plugin.get("checkboxes");
    checkboxPlugin.props.store.on(
      "updated",
      this.updateSelectionState.bind(this)
    );
  },
  initCsrf() {
    const meta: HTMLMetaElement | null = document.querySelector(
      "meta[name='csrf-token']"
    );
    this.csrf = meta?.content ?? "";
  },
  async loadData() {
    return new Promise((resolve, _) => {
      resolve(
        fakeData.data.map((record: any) => {
          return [
            record.id,
            record.code,
            record.httpmethod,
            // record.errormsg,
            // record.errortraceback,
            record.errortype,
            record.ip,
            record.postvalues,
            record.referrer,
            record.requestargs,
            record.requestpath,
            record.useragent,
            record.userbrowser,
            record.userbrowserversion,
            record.userplatform,
            record.when,
          ];
        })
      );
    });
    // const response = await fetch("/data", {
    //   headers: {
    //     "X-CSRFToken": this.csrf,
    //     "Content-Type": "application/json;charset=UTF-8",
    //   },
    // });
    // if (response.ok) {
    //   console.log(await response.json());
    // }
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
        // "Error message",
        // "Error traceback",
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
        limit: 5,
        summary: false,
      },
    });
    this.grid.on("ready", this.onGridReady.bind(this));
    this.grid.render(this.$refs["tableWrapper"]);
  },
}));

document.addEventListener("DOMContentLoaded", Alpine.start);
