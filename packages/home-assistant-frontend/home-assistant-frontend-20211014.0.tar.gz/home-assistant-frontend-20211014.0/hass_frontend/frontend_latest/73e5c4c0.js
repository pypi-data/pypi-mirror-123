/*! For license information please see 73e5c4c0.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[22179],{28417:(e,t,a)=>{a(50808);var o=a(33367),s=a(93592),i=a(87156);const l={getTabbableNodes:function(e){const t=[];return this._collectTabbableNodes(e,t)?s.H._sortByTabIndex(t):t},_collectTabbableNodes:function(e,t){if(e.nodeType!==Node.ELEMENT_NODE||!s.H._isVisible(e))return!1;const a=e,o=s.H._normalizedTabIndex(a);let l,n=o>0;o>=0&&t.push(a),l="content"===a.localName||"slot"===a.localName?(0,i.vz)(a).getDistributedNodes():(0,i.vz)(a.shadowRoot||a.root||a).children;for(let e=0;e<l.length;e++)n=this._collectTabbableNodes(l[e],t)||n;return n}},n=customElements.get("paper-dialog"),r={get _focusableNodes(){return l.getTabbableNodes(this)}};class d extends((0,o.P)([r],n)){}customElements.define("ha-paper-dialog",d)},22179:(e,t,a)=>{a.r(t);a(53918);var o=a(50856),s=a(28426),i=(a(28417),a(31206),a(55905),a(10983),a(1265));a(36436);class l extends((0,i.Z)(s.H3)){static get template(){return o.d`
      <style include="ha-style-dialog">
        .error {
          color: red;
        }
        @media all and (max-width: 500px) {
          ha-paper-dialog {
            margin: 0;
            width: 100%;
            max-height: calc(100% - var(--header-height));

            position: fixed !important;
            bottom: 0px;
            left: 0px;
            right: 0px;
            overflow: scroll;
            border-bottom-left-radius: 0px;
            border-bottom-right-radius: 0px;
          }
        }

        ha-paper-dialog {
          border-radius: 2px;
        }
        ha-paper-dialog p {
          color: var(--secondary-text-color);
        }

        .icon {
          float: right;
        }
      </style>
      <ha-paper-dialog
        id="mp3dialog"
        with-backdrop
        opened="{{_opened}}"
        on-opened-changed="_openedChanged"
      >
        <h2>
          [[localize('ui.panel.mailbox.playback_title')]]
          <div class="icon">
            <template is="dom-if" if="[[_loading]]">
              <ha-circular-progress active></ha-circular-progress>
            </template>
            <ha-icon-button id="delicon" on-click="openDeleteDialog">
              <ha-icon icon="hass:delete"></ha-icon>
            </ha-icon-button>
          </div>
        </h2>
        <div id="transcribe"></div>
        <div>
          <template is="dom-if" if="[[_errorMsg]]">
            <div class="error">[[_errorMsg]]</div>
          </template>
          <audio id="mp3" preload="none" controls>
            <source id="mp3src" src="" type="audio/mpeg" />
          </audio>
        </div>
      </ha-paper-dialog>
    `}static get properties(){return{hass:Object,_currentMessage:Object,_errorMsg:String,_loading:{type:Boolean,value:!1},_opened:{type:Boolean,value:!1}}}showDialog({hass:e,message:t}){this.hass=e,this._errorMsg=null,this._currentMessage=t,this._opened=!0,this.$.transcribe.innerText=t.message;const a=t.platform,o=this.$.mp3;if(a.has_media){o.style.display="",this._showLoading(!0),o.src=null;const e=`/api/mailbox/media/${a.name}/${t.sha}`;this.hass.fetchWithAuth(e).then((e=>e.ok?e.blob():Promise.reject({status:e.status,statusText:e.statusText}))).then((e=>{this._showLoading(!1),o.src=window.URL.createObjectURL(e),o.play()})).catch((e=>{this._showLoading(!1),this._errorMsg=`Error loading audio: ${e.statusText}`}))}else o.style.display="none",this._showLoading(!1)}openDeleteDialog(){confirm(this.localize("ui.panel.mailbox.delete_prompt"))&&this.deleteSelected()}deleteSelected(){const e=this._currentMessage;this.hass.callApi("DELETE",`mailbox/delete/${e.platform.name}/${e.sha}`),this._dialogDone()}_dialogDone(){this.$.mp3.pause(),this.setProperties({_currentMessage:null,_errorMsg:null,_loading:!1,_opened:!1})}_openedChanged(e){e.detail.value||this._dialogDone()}_showLoading(e){const t=this.$.delicon;if(e)this._loading=!0,t.style.display="none";else{const e=this._currentMessage.platform;this._loading=!1,t.style.display=e.can_delete?"":"none"}}}customElements.define("ha-dialog-show-audio-message",l)},36436:(e,t,a)=>{a(21384);var o=a(11654);const s=document.createElement("template");s.setAttribute("style","display: none;"),s.innerHTML=`<dom-module id="ha-style-dialog">\n<template>\n  <style>\n    ${o.yu.cssText}\n  </style>\n</template>\n</dom-module>`,document.head.appendChild(s.content)}}]);
//# sourceMappingURL=73e5c4c0.js.map