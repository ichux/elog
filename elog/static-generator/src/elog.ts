import Alpine from "alpinejs";
import { Grid } from "gridjs";
import { RowSelection } from "gridjs/plugins/selection";
import fakeData from "./faker";
import './gridjs.css'

Alpine.data("elog", () => ({
  grid: undefined as Grid | undefined,
  updateSelectionState(state: any, previousState: any) {
    console.log("Update: ", state, previousState);
  },
  onGridReady() {
    const checkboxPlugin = this.grid.config.plugin.get("checkboxes");
    checkboxPlugin.props.store.on("updated", this.updateSelectionState);
  },
  async loadData() {
    return new Promise((resolve, _) => {
      resolve(fakeData.data.map((record: any) => {
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
      }));
    });
  },
  async init(): Promise<void> {
    console.log("Aloaaaa :)")
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
      sort: true,
      resizable: true,
    });
    this.grid.on("ready", this.onGridReady.bind(this));
    this.grid.render(this.$refs["tableWrapper"]);
  },
}));

document.addEventListener("DOMContentLoaded", Alpine.start);
