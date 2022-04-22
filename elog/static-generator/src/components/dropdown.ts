import { LitElement, html } from "lit";
import { customElement, property } from "lit/decorators.js";

@customElement("el-dropdown")
class ElDropdownElement extends LitElement {
  @property()
  public text: string;

  @property()
  public actions: string;

  @property({type: Boolean})
  public disabled: boolean;

  constructor() {
    super();
    this.text = "";
    this.actions = "";
    this.disabled = false;
  }

  protected createRenderRoot(): Element | ShadowRoot {
    return this;
  }

  protected _emitSelectionEvent(selection: string) {
    console.log("dispatching selection");
    this.dispatchEvent(
      new CustomEvent("selection", {
        detail: {
          selection,
        },
        bubbles: true,
      })
    );
  }

  render() {
    return html`
      <div
        class="relative min-w-content bg-slate-900"
        x-data="{ open: false }"
        @click.outside="open = false"
      >
        <div class="h-full w-full" @click="open = !open">
          <button ?disabled=${this.disabled}
            class="h-full px-3 py-2 w-full flex items-center text-sm font-medium  text-white hover:text-gray-300 hover:border-gray-200 focus:outline-none focus:text-gray-300 focus:border-gray-300 transition duration-150 ease-in-out"
          >
            <span
              class="font-medium w-full h-full flex justify-center items-center"
              >${this.text}</span
            >
            <div class="ml-1 w-4 h-4">
              <svg
                class="w-4 h-4 fill-current"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
              >
                <path
                  fill-rule="evenodd"
                  d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                  clip-rule="evenodd"
                ></path>
              </svg>
            </div>
          </button>
        </div>
        <div
          x-show="open"
          x-transition:enter="transition ease-out duration-200"
          x-transition:enter-start="transform opacity-0 scale-95"
          x-transition:enter-end="transform opacity-100 scale-100"
          x-transition:leave="transition ease-in duration-75"
          x-transition:leave-start="transform opacity-100 scale-100"
          x-transition:leave-end="transform opacity-0 scale-95"
          class="absolute right-0 top-full z-50 w-48 mt-2 shadow-lg origin-top-right"
          @click="open = false"
        >
          ${this.actions.split(/,\s?/).map(
            (action) => html`
              <div class="py-0.5 bg-white ring-1 ring-black ring-opacity-5">
                <div>
                  <span
                    class="block px-3 py-2 text-sm text-gray-700 leading-5 hover:bg-gray-100 focus:outline-none focus:bg-gray-100 transition duration-150 ease-in-out"
                    x-on:click="$dispatch('selection', {selection: '${action}'})"
                    >${action}</span
                  >
                </div>
              </div>
            `
          )}
        </div>
      </div>
    `;
  }
}

declare global {
  interface HTMLElementTagNameMap {
    "el-dropdown": ElDropdownElement;
  }
}