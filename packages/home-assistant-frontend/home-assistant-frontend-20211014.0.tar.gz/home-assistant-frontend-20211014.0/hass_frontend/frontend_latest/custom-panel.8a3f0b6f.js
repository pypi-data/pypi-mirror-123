/*! For license information please see custom-panel.8a3f0b6f.js.LICENSE.txt */
(()=>{var e,t,o={47181:(e,t,o)=>{"use strict";o.d(t,{B:()=>r});const r=(e,t,o,r)=>{r=r||{},o=null==o?{}:o;const i=new Event(t,{bubbles:void 0===r.bubbles||r.bubbles,cancelable:Boolean(r.cancelable),composed:void 0===r.composed||r.composed});return i.detail=o,e.dispatchEvent(i),i}},37846:()=>{if(/^((?!chrome|android).)*version\/14\.0\s.*safari/i.test(navigator.userAgent)){const e=window.Element.prototype.attachShadow;window.Element.prototype.attachShadow=function(t){return t&&t.delegatesFocus&&delete t.delegatesFocus,e.apply(this,[t])}}},11654:(e,t,o)=>{"use strict";o.d(t,{_l:()=>i,q0:()=>l,Qx:()=>a,e$:()=>s});var r=o(7599);const i={"primary-background-color":"#111111","card-background-color":"#1c1c1c","secondary-background-color":"#202020","primary-text-color":"#e1e1e1","secondary-text-color":"#9b9b9b","disabled-text-color":"#6f6f6f","app-header-text-color":"#e1e1e1","app-header-background-color":"#101e24","switch-unchecked-button-color":"#999999","switch-unchecked-track-color":"#9b9b9b","divider-color":"rgba(225, 225, 225, .12)","mdc-ripple-color":"#AAAAAA","input-idle-line-color":"rgba(255, 255, 255, 0.42)","input-hover-line-color":"rgba(255, 255, 255, 0.87)","input-disabled-line-color":"rgba(255, 255, 255, 0.06)","input-outlined-idle-border-color":"rgba(255, 255, 255, 0.38)","input-outlined-hover-border-color":"rgba(255, 255, 255, 0.87)","input-outlined-disabled-border-color":"rgba(255, 255, 255, 0.06)","input-fill-color":"rgb(10, 10, 10)","input-disabled-fill-color":"rgb(5, 5, 5)","input-ink-color":"rgba(255, 255, 255, 0.87)","input-label-ink-color":"rgba(255, 255, 255, 0.6)","input-disabled-ink-color":"rgba(255, 255, 255, 0.37)","input-dropdown-icon-color":"rgba(255, 255, 255, 0.54)","codemirror-keyword":"#C792EA","codemirror-operator":"#89DDFF","codemirror-variable":"#f07178","codemirror-variable-2":"#EEFFFF","codemirror-variable-3":"#DECB6B","codemirror-builtin":"#FFCB6B","codemirror-atom":"#F78C6C","codemirror-number":"#FF5370","codemirror-def":"#82AAFF","codemirror-string":"#C3E88D","codemirror-string-2":"#f07178","codemirror-comment":"#545454","codemirror-tag":"#FF5370","codemirror-meta":"#FFCB6B","codemirror-attribute":"#C792EA","codemirror-property":"#C792EA","codemirror-qualifier":"#DECB6B","codemirror-type":"#DECB6B","energy-grid-return-color":"#b39bdb"},l={"state-icon-error-color":"var(--error-state-color, var(--error-color))","state-unavailable-color":"var(--state-icon-unavailable-color, var(--disabled-text-color))","sidebar-text-color":"var(--primary-text-color)","sidebar-background-color":"var(--card-background-color)","sidebar-selected-text-color":"var(--primary-color)","sidebar-selected-icon-color":"var(--primary-color)","sidebar-icon-color":"rgba(var(--rgb-primary-text-color), 0.6)","switch-checked-color":"var(--primary-color)","switch-checked-button-color":"var(--switch-checked-color, var(--primary-background-color))","switch-checked-track-color":"var(--switch-checked-color, #000000)","switch-unchecked-button-color":"var(--switch-unchecked-color, var(--primary-background-color))","switch-unchecked-track-color":"var(--switch-unchecked-color, #000000)","slider-color":"var(--primary-color)","slider-secondary-color":"var(--light-primary-color)","slider-track-color":"var(--scrollbar-thumb-color)","label-badge-background-color":"var(--card-background-color)","label-badge-text-color":"rgba(var(--rgb-primary-text-color), 0.8)","paper-listbox-background-color":"var(--card-background-color)","paper-item-icon-color":"var(--state-icon-color)","paper-item-icon-active-color":"var(--state-icon-active-color)","table-row-background-color":"var(--primary-background-color)","table-row-alternative-background-color":"var(--secondary-background-color)","paper-slider-knob-color":"var(--slider-color)","paper-slider-knob-start-color":"var(--slider-color)","paper-slider-pin-color":"var(--slider-color)","paper-slider-pin-start-color":"var(--slider-color)","paper-slider-active-color":"var(--slider-color)","paper-slider-secondary-color":"var(--slider-secondary-color)","paper-slider-container-color":"var(--slider-track-color)","data-table-background-color":"var(--card-background-color)","markdown-code-background-color":"var(--primary-background-color)","mdc-theme-primary":"var(--primary-color)","mdc-theme-secondary":"var(--accent-color)","mdc-theme-background":"var(--primary-background-color)","mdc-theme-surface":"var(--card-background-color)","mdc-theme-on-primary":"var(--text-primary-color)","mdc-theme-on-secondary":"var(--text-primary-color)","mdc-theme-on-surface":"var(--primary-text-color)","mdc-theme-text-disabled-on-light":"var(--disabled-text-color)","mdc-theme-text-primary-on-background":"var(--primary-text-color)","mdc-theme-text-secondary-on-background":"var(--secondary-text-color)","mdc-theme-text-icon-on-background":"var(--secondary-text-color)","mdc-theme-error":"var(--error-color)","app-header-text-color":"var(--text-primary-color)","app-header-background-color":"var(--primary-color)","mdc-checkbox-unchecked-color":"rgba(var(--rgb-primary-text-color), 0.54)","mdc-checkbox-disabled-color":"var(--disabled-text-color)","mdc-radio-unchecked-color":"rgba(var(--rgb-primary-text-color), 0.54)","mdc-radio-disabled-color":"var(--disabled-text-color)","mdc-tab-text-label-color-default":"var(--primary-text-color)","mdc-button-disabled-ink-color":"var(--disabled-text-color)","mdc-button-outline-color":"var(--divider-color)","mdc-dialog-scroll-divider-color":"var(--divider-color)","mdc-text-field-idle-line-color":"var(--input-idle-line-color)","mdc-text-field-hover-line-color":"var(--input-hover-line-color)","mdc-text-field-disabled-line-color":"var(--input-disabled-line-color)","mdc-text-field-outlined-idle-border-color":"var(--input-outlined-idle-border-color)","mdc-text-field-outlined-hover-border-color":"var(--input-outlined-hover-border-color)","mdc-text-field-outlined-disabled-border-color":"var(--input-outlined-disabled-border-color)","mdc-text-field-fill-color":"var(--input-fill-color)","mdc-text-field-disabled-fill-color":"var(--input-disabled-fill-color)","mdc-text-field-ink-color":"var(--input-ink-color)","mdc-text-field-label-ink-color":"var(--input-label-ink-color)","mdc-text-field-disabled-ink-color":"var(--input-disabled-ink-color)","mdc-select-idle-line-color":"var(--input-idle-line-color)","mdc-select-hover-line-color":"var(--input-hover-line-color)","mdc-select-outlined-idle-border-color":"var(--input-outlined-idle-border-color)","mdc-select-outlined-hover-border-color":"var(--input-outlined-hover-border-color)","mdc-select-outlined-disabled-border-color":"var(--input-outlined-disabled-border-color)","mdc-select-fill-color":"var(--input-fill-color)","mdc-select-disabled-fill-color":"var(--input-disabled-fill-color)","mdc-select-ink-color":"var(--input-ink-color)","mdc-select-label-ink-color":"var(--input-label-ink-color)","mdc-select-disabled-ink-color":"var(--input-disabled-ink-color)","mdc-select-dropdown-icon-color":"var(--input-dropdown-icon-color)","mdc-select-disabled-dropdown-icon-color":"var(--input-disabled-ink-color)","chip-background-color":"rgba(var(--rgb-primary-text-color), 0.15)","material-body-text-color":"var(--primary-text-color)","material-background-color":"var(--card-background-color)","material-secondary-background-color":"var(--secondary-background-color)","material-secondary-text-color":"var(--secondary-text-color)"},n=r.iv`
  button.link {
    background: none;
    color: inherit;
    border: none;
    padding: 0;
    font: inherit;
    text-align: left;
    text-decoration: underline;
    cursor: pointer;
  }
`,a=r.iv`
  :host {
    font-family: var(--paper-font-body1_-_font-family);
    -webkit-font-smoothing: var(--paper-font-body1_-_-webkit-font-smoothing);
    font-size: var(--paper-font-body1_-_font-size);
    font-weight: var(--paper-font-body1_-_font-weight);
    line-height: var(--paper-font-body1_-_line-height);
  }

  app-header-layout,
  ha-app-layout {
    background-color: var(--primary-background-color);
  }

  app-header,
  app-toolbar {
    background-color: var(--app-header-background-color);
    font-weight: 400;
    color: var(--app-header-text-color, white);
  }

  app-toolbar {
    height: var(--header-height);
  }

  app-header div[sticky] {
    height: 48px;
  }

  app-toolbar [main-title] {
    margin-left: 20px;
  }

  h1 {
    font-family: var(--paper-font-headline_-_font-family);
    -webkit-font-smoothing: var(--paper-font-headline_-_-webkit-font-smoothing);
    white-space: var(--paper-font-headline_-_white-space);
    overflow: var(--paper-font-headline_-_overflow);
    text-overflow: var(--paper-font-headline_-_text-overflow);
    font-size: var(--paper-font-headline_-_font-size);
    font-weight: var(--paper-font-headline_-_font-weight);
    line-height: var(--paper-font-headline_-_line-height);
  }

  h2 {
    font-family: var(--paper-font-title_-_font-family);
    -webkit-font-smoothing: var(--paper-font-title_-_-webkit-font-smoothing);
    white-space: var(--paper-font-title_-_white-space);
    overflow: var(--paper-font-title_-_overflow);
    text-overflow: var(--paper-font-title_-_text-overflow);
    font-size: var(--paper-font-title_-_font-size);
    font-weight: var(--paper-font-title_-_font-weight);
    line-height: var(--paper-font-title_-_line-height);
  }

  h3 {
    font-family: var(--paper-font-subhead_-_font-family);
    -webkit-font-smoothing: var(--paper-font-subhead_-_-webkit-font-smoothing);
    white-space: var(--paper-font-subhead_-_white-space);
    overflow: var(--paper-font-subhead_-_overflow);
    text-overflow: var(--paper-font-subhead_-_text-overflow);
    font-size: var(--paper-font-subhead_-_font-size);
    font-weight: var(--paper-font-subhead_-_font-weight);
    line-height: var(--paper-font-subhead_-_line-height);
  }

  a {
    color: var(--primary-color);
  }

  .secondary {
    color: var(--secondary-text-color);
  }

  .error {
    color: var(--error-color);
  }

  .warning {
    color: var(--error-color);
  }

  mwc-button.warning {
    --mdc-theme-primary: var(--error-color);
  }

  ${n}

  .card-actions a {
    text-decoration: none;
  }

  .card-actions .warning {
    --mdc-theme-primary: var(--error-color);
  }

  .layout.horizontal,
  .layout.vertical {
    display: flex;
  }
  .layout.inline {
    display: inline-flex;
  }
  .layout.horizontal {
    flex-direction: row;
  }
  .layout.vertical {
    flex-direction: column;
  }
  .layout.wrap {
    flex-wrap: wrap;
  }
  .layout.no-wrap {
    flex-wrap: nowrap;
  }
  .layout.center,
  .layout.center-center {
    align-items: center;
  }
  .layout.bottom {
    align-items: flex-end;
  }
  .layout.center-justified,
  .layout.center-center {
    justify-content: center;
  }
  .flex {
    flex: 1;
    flex-basis: 0.000000001px;
  }
  .flex-auto {
    flex: 1 1 auto;
  }
  .flex-none {
    flex: none;
  }
  .layout.justified {
    justify-content: space-between;
  }
`,s=(r.iv`
  /* prevent clipping of positioned elements */
  paper-dialog-scrollable {
    --paper-dialog-scrollable: {
      -webkit-overflow-scrolling: auto;
    }
  }

  /* force smooth scrolling for iOS 10 */
  paper-dialog-scrollable.can-scroll {
    --paper-dialog-scrollable: {
      -webkit-overflow-scrolling: touch;
    }
  }

  .paper-dialog-buttons {
    align-items: flex-end;
    padding: 8px;
    padding-bottom: max(env(safe-area-inset-bottom), 8px);
  }

  @media all and (min-width: 450px) and (min-height: 500px) {
    ha-paper-dialog {
      min-width: 400px;
    }
  }

  @media all and (max-width: 450px), all and (max-height: 500px) {
    paper-dialog,
    ha-paper-dialog {
      margin: 0;
      width: calc(
        100% - env(safe-area-inset-right) - env(safe-area-inset-left)
      ) !important;
      min-width: calc(
        100% - env(safe-area-inset-right) - env(safe-area-inset-left)
      ) !important;
      max-width: calc(
        100% - env(safe-area-inset-right) - env(safe-area-inset-left)
      ) !important;
      max-height: calc(100% - var(--header-height));

      position: fixed !important;
      bottom: 0px;
      left: env(safe-area-inset-left);
      right: env(safe-area-inset-right);
      overflow: scroll;
      border-bottom-left-radius: 0px;
      border-bottom-right-radius: 0px;
    }
  }

  /* mwc-dialog (ha-dialog) styles */
  ha-dialog {
    --mdc-dialog-min-width: 400px;
    --mdc-dialog-max-width: 600px;
    --mdc-dialog-heading-ink-color: var(--primary-text-color);
    --mdc-dialog-content-ink-color: var(--primary-text-color);
    --justify-action-buttons: space-between;
  }

  ha-dialog .form {
    padding-bottom: 24px;
    color: var(--primary-text-color);
  }

  a {
    color: var(--primary-color);
  }

  /* make dialog fullscreen on small screens */
  @media all and (max-width: 450px), all and (max-height: 500px) {
    ha-dialog {
      --mdc-dialog-min-width: calc(
        100vw - env(safe-area-inset-right) - env(safe-area-inset-left)
      );
      --mdc-dialog-max-width: calc(
        100vw - env(safe-area-inset-right) - env(safe-area-inset-left)
      );
      --mdc-dialog-min-height: 100%;
      --mdc-dialog-max-height: 100%;
      --mdc-shape-medium: 0px;
      --vertial-align-dialog: flex-end;
    }
  }
  mwc-button.warning {
    --mdc-theme-primary: var(--error-color);
  }
  .error {
    color: var(--error-color);
  }
`,r.iv`
  .ha-scrollbar::-webkit-scrollbar {
    width: 0.4rem;
    height: 0.4rem;
  }

  .ha-scrollbar::-webkit-scrollbar-thumb {
    -webkit-border-radius: 4px;
    border-radius: 4px;
    background: var(--scrollbar-thumb-color);
  }

  .ha-scrollbar {
    overflow-y: auto;
    scrollbar-color: var(--scrollbar-thumb-color) transparent;
    scrollbar-width: thin;
  }
`,r.iv`
  body {
    background-color: var(--primary-background-color);
    color: var(--primary-text-color);
    height: calc(100vh - 32px);
    width: 100vw;
  }
`)},1575:(e,t,o)=>{"use strict";o.d(t,{fl:()=>b,iv:()=>s});const r=window.ShadowRoot&&(void 0===window.ShadyCSS||window.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,i=Symbol(),l=new Map;class n{constructor(e,t){if(this._$cssResult$=!0,t!==i)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=e}get styleSheet(){let e=l.get(this.cssText);return r&&void 0===e&&(l.set(this.cssText,e=new CSSStyleSheet),e.replaceSync(this.cssText)),e}toString(){return this.cssText}}const a=e=>new n("string"==typeof e?e:e+"",i),s=(e,...t)=>{const o=1===e.length?e[0]:t.reduce(((t,o,r)=>t+(e=>{if(!0===e._$cssResult$)return e.cssText;if("number"==typeof e)return e;throw Error("Value passed to 'css' function must be a 'css' function result: "+e+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(o)+e[r+1]),e[0]);return new n(o,i)},c=(e,t)=>{r?e.adoptedStyleSheets=t.map((e=>e instanceof CSSStyleSheet?e:e.styleSheet)):t.forEach((t=>{const o=document.createElement("style"),r=window.litNonce;void 0!==r&&o.setAttribute("nonce",r),o.textContent=t.cssText,e.appendChild(o)}))},d=r?e=>e:e=>e instanceof CSSStyleSheet?(e=>{let t="";for(const o of e.cssRules)t+=o.cssText;return a(t)})(e):e;var h,p;const u={toAttribute(e,t){switch(t){case Boolean:e=e?"":null;break;case Object:case Array:e=null==e?e:JSON.stringify(e)}return e},fromAttribute(e,t){let o=e;switch(t){case Boolean:o=null!==e;break;case Number:o=null===e?null:Number(e);break;case Object:case Array:try{o=JSON.parse(e)}catch(e){o=null}}return o}},v=(e,t)=>t!==e&&(t==t||e==e),m={attribute:!0,type:String,converter:u,reflect:!1,hasChanged:v};class b extends HTMLElement{constructor(){super(),this._$Et=new Map,this.isUpdatePending=!1,this.hasUpdated=!1,this._$Ei=null,this.o()}static addInitializer(e){var t;null!==(t=this.l)&&void 0!==t||(this.l=[]),this.l.push(e)}static get observedAttributes(){this.finalize();const e=[];return this.elementProperties.forEach(((t,o)=>{const r=this._$Eh(o,t);void 0!==r&&(this._$Eu.set(r,o),e.push(r))})),e}static createProperty(e,t=m){if(t.state&&(t.attribute=!1),this.finalize(),this.elementProperties.set(e,t),!t.noAccessor&&!this.prototype.hasOwnProperty(e)){const o="symbol"==typeof e?Symbol():"__"+e,r=this.getPropertyDescriptor(e,o,t);void 0!==r&&Object.defineProperty(this.prototype,e,r)}}static getPropertyDescriptor(e,t,o){return{get(){return this[t]},set(r){const i=this[e];this[t]=r,this.requestUpdate(e,i,o)},configurable:!0,enumerable:!0}}static getPropertyOptions(e){return this.elementProperties.get(e)||m}static finalize(){if(this.hasOwnProperty("finalized"))return!1;this.finalized=!0;const e=Object.getPrototypeOf(this);if(e.finalize(),this.elementProperties=new Map(e.elementProperties),this._$Eu=new Map,this.hasOwnProperty("properties")){const e=this.properties,t=[...Object.getOwnPropertyNames(e),...Object.getOwnPropertySymbols(e)];for(const o of t)this.createProperty(o,e[o])}return this.elementStyles=this.finalizeStyles(this.styles),!0}static finalizeStyles(e){const t=[];if(Array.isArray(e)){const o=new Set(e.flat(1/0).reverse());for(const e of o)t.unshift(d(e))}else void 0!==e&&t.push(d(e));return t}static _$Eh(e,t){const o=t.attribute;return!1===o?void 0:"string"==typeof o?o:"string"==typeof e?e.toLowerCase():void 0}o(){var e;this._$Ev=new Promise((e=>this.enableUpdating=e)),this._$AL=new Map,this._$Ep(),this.requestUpdate(),null===(e=this.constructor.l)||void 0===e||e.forEach((e=>e(this)))}addController(e){var t,o;(null!==(t=this._$Em)&&void 0!==t?t:this._$Em=[]).push(e),void 0!==this.renderRoot&&this.isConnected&&(null===(o=e.hostConnected)||void 0===o||o.call(e))}removeController(e){var t;null===(t=this._$Em)||void 0===t||t.splice(this._$Em.indexOf(e)>>>0,1)}_$Ep(){this.constructor.elementProperties.forEach(((e,t)=>{this.hasOwnProperty(t)&&(this._$Et.set(t,this[t]),delete this[t])}))}createRenderRoot(){var e;const t=null!==(e=this.shadowRoot)&&void 0!==e?e:this.attachShadow(this.constructor.shadowRootOptions);return c(t,this.constructor.elementStyles),t}connectedCallback(){var e;void 0===this.renderRoot&&(this.renderRoot=this.createRenderRoot()),this.enableUpdating(!0),null===(e=this._$Em)||void 0===e||e.forEach((e=>{var t;return null===(t=e.hostConnected)||void 0===t?void 0:t.call(e)}))}enableUpdating(e){}disconnectedCallback(){var e;null===(e=this._$Em)||void 0===e||e.forEach((e=>{var t;return null===(t=e.hostDisconnected)||void 0===t?void 0:t.call(e)}))}attributeChangedCallback(e,t,o){this._$AK(e,o)}_$Eg(e,t,o=m){var r,i;const l=this.constructor._$Eh(e,o);if(void 0!==l&&!0===o.reflect){const n=(null!==(i=null===(r=o.converter)||void 0===r?void 0:r.toAttribute)&&void 0!==i?i:u.toAttribute)(t,o.type);this._$Ei=e,null==n?this.removeAttribute(l):this.setAttribute(l,n),this._$Ei=null}}_$AK(e,t){var o,r,i;const l=this.constructor,n=l._$Eu.get(e);if(void 0!==n&&this._$Ei!==n){const e=l.getPropertyOptions(n),a=e.converter,s=null!==(i=null!==(r=null===(o=a)||void 0===o?void 0:o.fromAttribute)&&void 0!==r?r:"function"==typeof a?a:null)&&void 0!==i?i:u.fromAttribute;this._$Ei=n,this[n]=s(t,e.type),this._$Ei=null}}requestUpdate(e,t,o){let r=!0;void 0!==e&&(((o=o||this.constructor.getPropertyOptions(e)).hasChanged||v)(this[e],t)?(this._$AL.has(e)||this._$AL.set(e,t),!0===o.reflect&&this._$Ei!==e&&(void 0===this._$ES&&(this._$ES=new Map),this._$ES.set(e,o))):r=!1),!this.isUpdatePending&&r&&(this._$Ev=this._$EC())}async _$EC(){this.isUpdatePending=!0;try{await this._$Ev}catch(e){Promise.reject(e)}const e=this.scheduleUpdate();return null!=e&&await e,!this.isUpdatePending}scheduleUpdate(){return this.performUpdate()}performUpdate(){var e;if(!this.isUpdatePending)return;this.hasUpdated,this._$Et&&(this._$Et.forEach(((e,t)=>this[t]=e)),this._$Et=void 0);let t=!1;const o=this._$AL;try{t=this.shouldUpdate(o),t?(this.willUpdate(o),null===(e=this._$Em)||void 0===e||e.forEach((e=>{var t;return null===(t=e.hostUpdate)||void 0===t?void 0:t.call(e)})),this.update(o)):this._$ET()}catch(e){throw t=!1,this._$ET(),e}t&&this._$AE(o)}willUpdate(e){}_$AE(e){var t;null===(t=this._$Em)||void 0===t||t.forEach((e=>{var t;return null===(t=e.hostUpdated)||void 0===t?void 0:t.call(e)})),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(e)),this.updated(e)}_$ET(){this._$AL=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$Ev}shouldUpdate(e){return!0}update(e){void 0!==this._$ES&&(this._$ES.forEach(((e,t)=>this._$Eg(t,this[t],e))),this._$ES=void 0),this._$ET()}updated(e){}firstUpdated(e){}}b.finalized=!0,b.elementProperties=new Map,b.elementStyles=[],b.shadowRootOptions={mode:"open"},null===(h=globalThis.reactiveElementPolyfillSupport)||void 0===h||h.call(globalThis,{ReactiveElement:b}),(null!==(p=globalThis.reactiveElementVersions)&&void 0!==p?p:globalThis.reactiveElementVersions=[]).push("1.0.0")},79899:(e,t,o)=>{"use strict";o.d(t,{iv:()=>n.iv,dy:()=>a.dy,YP:()=>a.YP,oi:()=>s});var r,i,l,n=o(1575),a=o(15304);class s extends n.fl{constructor(){super(...arguments),this.renderOptions={host:this},this._$Dt=void 0}createRenderRoot(){var e,t;const o=super.createRenderRoot();return null!==(e=(t=this.renderOptions).renderBefore)&&void 0!==e||(t.renderBefore=o.firstChild),o}update(e){const t=this.render();this.hasUpdated||(this.renderOptions.isConnected=this.isConnected),super.update(e),this._$Dt=(0,a.sY)(t,this.renderRoot,this.renderOptions)}connectedCallback(){var e;super.connectedCallback(),null===(e=this._$Dt)||void 0===e||e.setConnected(!0)}disconnectedCallback(){var e;super.disconnectedCallback(),null===(e=this._$Dt)||void 0===e||e.setConnected(!1)}render(){return a.Jb}}s.finalized=!0,s._$litElement$=!0,null===(r=globalThis.litElementHydrateSupport)||void 0===r||r.call(globalThis,{LitElement:s}),null===(i=globalThis.litElementPolyfillSupport)||void 0===i||i.call(globalThis,{LitElement:s});(null!==(l=globalThis.litElementVersions)&&void 0!==l?l:globalThis.litElementVersions=[]).push("3.0.0")},15304:(e,t,o)=>{"use strict";var r,i;o.d(t,{dy:()=>x,Jb:()=>k,Ld:()=>E,sY:()=>C,YP:()=>A});const l=globalThis.trustedTypes,n=l?l.createPolicy("lit-html",{createHTML:e=>e}):void 0,a=`lit$${(Math.random()+"").slice(9)}$`,s="?"+a,c=`<${s}>`,d=document,h=(e="")=>d.createComment(e),p=e=>null===e||"object"!=typeof e&&"function"!=typeof e,u=Array.isArray,v=e=>{var t;return u(e)||"function"==typeof(null===(t=e)||void 0===t?void 0:t[Symbol.iterator])},m=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,b=/-->/g,f=/>/g,g=/>|[ 	\n\r](?:([^\s"'>=/]+)([ 	\n\r]*=[ 	\n\r]*(?:[^ 	\n\r"'`<>=]|("|')|))|$)/g,y=/'/g,_=/"/g,w=/^(?:script|style|textarea)$/i,$=e=>(t,...o)=>({_$litType$:e,strings:t,values:o}),x=$(1),A=$(2),k=Symbol.for("lit-noChange"),E=Symbol.for("lit-nothing"),S=new WeakMap,C=(e,t,o)=>{var r,i;const l=null!==(r=null==o?void 0:o.renderBefore)&&void 0!==r?r:t;let n=l._$litPart$;if(void 0===n){const e=null!==(i=null==o?void 0:o.renderBefore)&&void 0!==i?i:null;l._$litPart$=n=new N(t.insertBefore(h(),e),e,void 0,null!=o?o:{})}return n._$AI(e),n},P=d.createTreeWalker(d,129,null,!1),T=(e,t)=>{const o=e.length-1,r=[];let i,l=2===t?"<svg>":"",s=m;for(let t=0;t<o;t++){const o=e[t];let n,d,h=-1,p=0;for(;p<o.length&&(s.lastIndex=p,d=s.exec(o),null!==d);)p=s.lastIndex,s===m?"!--"===d[1]?s=b:void 0!==d[1]?s=f:void 0!==d[2]?(w.test(d[2])&&(i=RegExp("</"+d[2],"g")),s=g):void 0!==d[3]&&(s=g):s===g?">"===d[0]?(s=null!=i?i:m,h=-1):void 0===d[1]?h=-2:(h=s.lastIndex-d[2].length,n=d[1],s=void 0===d[3]?g:'"'===d[3]?_:y):s===_||s===y?s=g:s===b||s===f?s=m:(s=g,i=void 0);const u=s===g&&e[t+1].startsWith("/>")?" ":"";l+=s===m?o+c:h>=0?(r.push(n),o.slice(0,h)+"$lit$"+o.slice(h)+a+u):o+a+(-2===h?(r.push(void 0),t):u)}const d=l+(e[o]||"<?>")+(2===t?"</svg>":"");return[void 0!==n?n.createHTML(d):d,r]};class U{constructor({strings:e,_$litType$:t},o){let r;this.parts=[];let i=0,n=0;const c=e.length-1,d=this.parts,[p,u]=T(e,t);if(this.el=U.createElement(p,o),P.currentNode=this.el.content,2===t){const e=this.el.content,t=e.firstChild;t.remove(),e.append(...t.childNodes)}for(;null!==(r=P.nextNode())&&d.length<c;){if(1===r.nodeType){if(r.hasAttributes()){const e=[];for(const t of r.getAttributeNames())if(t.endsWith("$lit$")||t.startsWith(a)){const o=u[n++];if(e.push(t),void 0!==o){const e=r.getAttribute(o.toLowerCase()+"$lit$").split(a),t=/([.?@])?(.*)/.exec(o);d.push({type:1,index:i,name:t[2],strings:e,ctor:"."===t[1]?j:"?"===t[1]?B:"@"===t[1]?R:M})}else d.push({type:6,index:i})}for(const t of e)r.removeAttribute(t)}if(w.test(r.tagName)){const e=r.textContent.split(a),t=e.length-1;if(t>0){r.textContent=l?l.emptyScript:"";for(let o=0;o<t;o++)r.append(e[o],h()),P.nextNode(),d.push({type:2,index:++i});r.append(e[t],h())}}}else if(8===r.nodeType)if(r.data===s)d.push({type:2,index:i});else{let e=-1;for(;-1!==(e=r.data.indexOf(a,e+1));)d.push({type:7,index:i}),e+=a.length-1}i++}}static createElement(e,t){const o=d.createElement("template");return o.innerHTML=e,o}}function H(e,t,o=e,r){var i,l,n,a;if(t===k)return t;let s=void 0!==r?null===(i=o._$Cl)||void 0===i?void 0:i[r]:o._$Cu;const c=p(t)?void 0:t._$litDirective$;return(null==s?void 0:s.constructor)!==c&&(null===(l=null==s?void 0:s._$AO)||void 0===l||l.call(s,!1),void 0===c?s=void 0:(s=new c(e),s._$AT(e,o,r)),void 0!==r?(null!==(n=(a=o)._$Cl)&&void 0!==n?n:a._$Cl=[])[r]=s:o._$Cu=s),void 0!==s&&(t=H(e,s._$AS(e,t.values),s,r)),t}class O{constructor(e,t){this.v=[],this._$AN=void 0,this._$AD=e,this._$AM=t}get parentNode(){return this._$AM.parentNode}get _$AU(){return this._$AM._$AU}p(e){var t;const{el:{content:o},parts:r}=this._$AD,i=(null!==(t=null==e?void 0:e.creationScope)&&void 0!==t?t:d).importNode(o,!0);P.currentNode=i;let l=P.nextNode(),n=0,a=0,s=r[0];for(;void 0!==s;){if(n===s.index){let t;2===s.type?t=new N(l,l.nextSibling,this,e):1===s.type?t=new s.ctor(l,s.name,s.strings,this,e):6===s.type&&(t=new L(l,this,e)),this.v.push(t),s=r[++a]}n!==(null==s?void 0:s.index)&&(l=P.nextNode(),n++)}return i}m(e){let t=0;for(const o of this.v)void 0!==o&&(void 0!==o.strings?(o._$AI(e,o,t),t+=o.strings.length-2):o._$AI(e[t])),t++}}class N{constructor(e,t,o,r){var i;this.type=2,this._$AH=E,this._$AN=void 0,this._$AA=e,this._$AB=t,this._$AM=o,this.options=r,this._$Cg=null===(i=null==r?void 0:r.isConnected)||void 0===i||i}get _$AU(){var e,t;return null!==(t=null===(e=this._$AM)||void 0===e?void 0:e._$AU)&&void 0!==t?t:this._$Cg}get parentNode(){let e=this._$AA.parentNode;const t=this._$AM;return void 0!==t&&11===e.nodeType&&(e=t.parentNode),e}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(e,t=this){e=H(this,e,t),p(e)?e===E||null==e||""===e?(this._$AH!==E&&this._$AR(),this._$AH=E):e!==this._$AH&&e!==k&&this.$(e):void 0!==e._$litType$?this.T(e):void 0!==e.nodeType?this.S(e):v(e)?this.M(e):this.$(e)}A(e,t=this._$AB){return this._$AA.parentNode.insertBefore(e,t)}S(e){this._$AH!==e&&(this._$AR(),this._$AH=this.A(e))}$(e){this._$AH!==E&&p(this._$AH)?this._$AA.nextSibling.data=e:this.S(d.createTextNode(e)),this._$AH=e}T(e){var t;const{values:o,_$litType$:r}=e,i="number"==typeof r?this._$AC(e):(void 0===r.el&&(r.el=U.createElement(r.h,this.options)),r);if((null===(t=this._$AH)||void 0===t?void 0:t._$AD)===i)this._$AH.m(o);else{const e=new O(i,this),t=e.p(this.options);e.m(o),this.S(t),this._$AH=e}}_$AC(e){let t=S.get(e.strings);return void 0===t&&S.set(e.strings,t=new U(e)),t}M(e){u(this._$AH)||(this._$AH=[],this._$AR());const t=this._$AH;let o,r=0;for(const i of e)r===t.length?t.push(o=new N(this.A(h()),this.A(h()),this,this.options)):o=t[r],o._$AI(i),r++;r<t.length&&(this._$AR(o&&o._$AB.nextSibling,r),t.length=r)}_$AR(e=this._$AA.nextSibling,t){var o;for(null===(o=this._$AP)||void 0===o||o.call(this,!1,!0,t);e&&e!==this._$AB;){const t=e.nextSibling;e.remove(),e=t}}setConnected(e){var t;void 0===this._$AM&&(this._$Cg=e,null===(t=this._$AP)||void 0===t||t.call(this,e))}}class M{constructor(e,t,o,r,i){this.type=1,this._$AH=E,this._$AN=void 0,this.element=e,this.name=t,this._$AM=r,this.options=i,o.length>2||""!==o[0]||""!==o[1]?(this._$AH=Array(o.length-1).fill(new String),this.strings=o):this._$AH=E}get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}_$AI(e,t=this,o,r){const i=this.strings;let l=!1;if(void 0===i)e=H(this,e,t,0),l=!p(e)||e!==this._$AH&&e!==k,l&&(this._$AH=e);else{const r=e;let n,a;for(e=i[0],n=0;n<i.length-1;n++)a=H(this,r[o+n],t,n),a===k&&(a=this._$AH[n]),l||(l=!p(a)||a!==this._$AH[n]),a===E?e=E:e!==E&&(e+=(null!=a?a:"")+i[n+1]),this._$AH[n]=a}l&&!r&&this.k(e)}k(e){e===E?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,null!=e?e:"")}}class j extends M{constructor(){super(...arguments),this.type=3}k(e){this.element[this.name]=e===E?void 0:e}}class B extends M{constructor(){super(...arguments),this.type=4}k(e){e&&e!==E?this.element.setAttribute(this.name,""):this.element.removeAttribute(this.name)}}class R extends M{constructor(e,t,o,r,i){super(e,t,o,r,i),this.type=5}_$AI(e,t=this){var o;if((e=null!==(o=H(this,e,t,0))&&void 0!==o?o:E)===k)return;const r=this._$AH,i=e===E&&r!==E||e.capture!==r.capture||e.once!==r.once||e.passive!==r.passive,l=e!==E&&(r===E||i);i&&this.element.removeEventListener(this.name,this,r),l&&this.element.addEventListener(this.name,this,e),this._$AH=e}handleEvent(e){var t,o;"function"==typeof this._$AH?this._$AH.call(null!==(o=null===(t=this.options)||void 0===t?void 0:t.host)&&void 0!==o?o:this.element,e):this._$AH.handleEvent(e)}}class L{constructor(e,t,o){this.element=e,this.type=6,this._$AN=void 0,this._$AM=t,this.options=o}get _$AU(){return this._$AM._$AU}_$AI(e){H(this,e)}}null===(r=globalThis.litHtmlPolyfillSupport)||void 0===r||r.call(globalThis,U,N),(null!==(i=globalThis.litHtmlVersions)&&void 0!==i?i:globalThis.litHtmlVersions=[]).push("2.0.0")},7599:(e,t,o)=>{"use strict";o.d(t,{oi:()=>r.oi,iv:()=>r.iv,dy:()=>r.dy,YP:()=>r.YP});o(1575),o(15304);var r=o(79899)}},r={};function i(e){var t=r[e];if(void 0!==t)return t.exports;var l=r[e]={exports:{}};return o[e](l,l.exports,i),l.exports}i.m=o,i.d=(e,t)=>{for(var o in t)i.o(t,o)&&!i.o(e,o)&&Object.defineProperty(e,o,{enumerable:!0,get:t[o]})},i.f={},i.e=e=>Promise.all(Object.keys(i.f).reduce(((t,o)=>(i.f[o](e,t),t)),[])),i.u=e=>({16134:"f592bb5e",43835:"401f3e95",48811:"3168e5c1",78309:"25e453f6",82678:"d63330b2"}[e]+".js"),i.o=(e,t)=>Object.prototype.hasOwnProperty.call(e,t),e={},t="home-assistant-frontend:",i.l=(o,r,l,n)=>{if(e[o])e[o].push(r);else{var a,s;if(void 0!==l)for(var c=document.getElementsByTagName("script"),d=0;d<c.length;d++){var h=c[d];if(h.getAttribute("src")==o||h.getAttribute("data-webpack")==t+l){a=h;break}}a||(s=!0,(a=document.createElement("script")).charset="utf-8",a.timeout=120,i.nc&&a.setAttribute("nonce",i.nc),a.setAttribute("data-webpack",t+l),a.src=o),e[o]=[r];var p=(t,r)=>{a.onerror=a.onload=null,clearTimeout(u);var i=e[o];if(delete e[o],a.parentNode&&a.parentNode.removeChild(a),i&&i.forEach((e=>e(r))),t)return t(r)},u=setTimeout(p.bind(null,void 0,{type:"timeout",target:a}),12e4);a.onerror=p.bind(null,a.onerror),a.onload=p.bind(null,a.onload),s&&document.head.appendChild(a)}},i.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},i.p="/frontend_latest/",(()=>{var e={28017:0};i.f.j=(t,o)=>{var r=i.o(e,t)?e[t]:void 0;if(0!==r)if(r)o.push(r[2]);else{var l=new Promise(((o,i)=>r=e[t]=[o,i]));o.push(r[2]=l);var n=i.p+i.u(t),a=new Error;i.l(n,(o=>{if(i.o(e,t)&&(0!==(r=e[t])&&(e[t]=void 0),r)){var l=o&&("load"===o.type?"missing":o.type),n=o&&o.target&&o.target.src;a.message="Loading chunk "+t+" failed.\n("+l+": "+n+")",a.name="ChunkLoadError",a.type=l,a.request=n,r[1](a)}}),"chunk-"+t,t)}};var t=(t,o)=>{var r,l,[n,a,s]=o,c=0;if(n.some((t=>0!==e[t]))){for(r in a)i.o(a,r)&&(i.m[r]=a[r]);if(s)s(i)}for(t&&t(o);c<n.length;c++)l=n[c],i.o(e,l)&&e[l]&&e[l][0](),e[n[c]]=0},o=self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[];o.forEach(t.bind(null,0)),o.push=t.bind(null,o.push.bind(o))})(),(()=>{"use strict";i(37846);var e=i(47181);const t=(e,t,o)=>new Promise(((r,i)=>{const l=document.createElement(e);let n="src",a="body";switch(l.onload=()=>r(t),l.onerror=()=>i(t),e){case"script":l.async=!0,o&&(l.type=o);break;case"link":l.type="text/css",l.rel="stylesheet",n="href",a="head"}l[n]=t,document[a].appendChild(l)})),o=e=>t("script",e),r="customElements"in window&&"content"in document.createElement("template"),l="ha-main-window",n=window.name===l?window:parent.name===l?parent:top;var a=i(11654);const s={},c=e=>{const r=(e=>e.html_url?{type:"html",url:e.html_url}:e.module_url&&e.js_url||e.module_url?{type:"module",url:e.module_url}:{type:"js",url:e.js_url})(e);return"js"===r.type?(r.url in s||(s[r.url]=o(r.url)),s[r.url]):"module"===r.type?(i=r.url,t("script",i,"module")):Promise.reject("No valid url found in panel config.");var i};let d,h;function p(e){h&&((e,t)=>{"setProperties"in e?e.setProperties(t):Object.keys(t).forEach((o=>{e[o]=t[o]}))})(h,e)}function u(t,l){const s=document.createElement("style");s.innerHTML="body { margin:0; } \n  @media (prefers-color-scheme: dark) {\n    body {\n      background-color: #111111;\n      color: #e1e1e1;\n    }\n  }",document.head.appendChild(s);const u=t.config._panel_custom;let v=Promise.resolve();r||(v=v.then((()=>o("/static/polyfills/webcomponents-bundle.js")))),v.then((()=>c(u))).then((()=>d||Promise.resolve())).then((()=>{h=(e=>{const t="html_url"in e?`ha-panel-${e.name}`:e.name;return document.createElement(t)})(u);h.addEventListener("hass-toggle-menu",(t=>{window.parent.customPanel&&(0,e.B)(window.parent.customPanel,t.type,t.detail)})),window.addEventListener("location-changed",(e=>{window.parent.customPanel&&window.parent.customPanel.navigate(window.location.pathname,e.detail)})),p({panel:t,...l}),document.body.appendChild(h)}),(e=>{let o;console.error(e,t),"hassio"===t.url_path?(Promise.all([i.e(78309),i.e(43835),i.e(16134),i.e(82678)]).then(i.bind(i,82678)),o=document.createElement("supervisor-error-screen")):(Promise.all([i.e(78309),i.e(16134),i.e(48811)]).then(i.bind(i,48811)),o=document.createElement("hass-error-screen"),o.error=`Unable to load the panel source: ${e}.`);const r=document.createElement("style");r.innerHTML=a.e$.cssText,document.body.appendChild(r),o.hass=l.hass,document.body.appendChild(o)})),document.body.addEventListener("click",(t=>{const o=(e=>{if(e.defaultPrevented||0!==e.button||e.metaKey||e.ctrlKey||e.shiftKey)return;const t=e.composedPath().filter((e=>"A"===e.tagName))[0];if(!t||t.target||t.hasAttribute("download")||"external"===t.getAttribute("rel"))return;let o=t.href;if(!o||-1!==o.indexOf("mailto:"))return;const r=window.location,i=r.origin||r.protocol+"//"+r.host;return 0===o.indexOf(i)&&(o=o.substr(i.length),"#"!==o)?(e.preventDefault(),o):void 0})(t);o&&((t,o)=>{const r=(null==o?void 0:o.replace)||!1;var i;r?n.history.replaceState(null!==(i=n.history.state)&&void 0!==i&&i.root?{root:!0}:null,"",t):n.history.pushState(null,"",t),(0,e.B)(n,"location-changed",{replace:r})})(o)}))}window.loadES5Adapter=()=>(d||(d=o("/static/polyfills/custom-elements-es5-adapter.js").catch()),d),document.addEventListener("DOMContentLoaded",(()=>window.parent.customPanel.registerIframe(u,p)),{once:!0})})()})();
//# sourceMappingURL=custom-panel.8a3f0b6f.js.map