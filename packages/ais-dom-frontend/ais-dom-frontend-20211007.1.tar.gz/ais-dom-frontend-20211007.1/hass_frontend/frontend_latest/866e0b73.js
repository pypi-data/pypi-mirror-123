"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[4705],{4705:(e,t,a)=>{a.r(t);a(12730);var l=a(50856),o=a(28426);a(48932),a(3426);class n extends o.H3{static get template(){return l.d`
      <style include="ha-style">
        iframe {
          border: 0;
          width: 100%;
          position: absolute;
          height: calc(100% - var(--header-height));
          background-color: var(--primary-background-color);
        }
      </style>
      <app-toolbar>
        <ha-menu-button hass="[[hass]]" narrow="[[narrow]]"></ha-menu-button>
        <div main-title>[[panel.title]]</div>
      </app-toolbar>

      <iframe
        src="[[panel.config.url]]"
        sandbox="allow-forms allow-popups allow-pointer-lock allow-same-origin allow-scripts allow-modals allow-download"
        allowfullscreen="true"
        webkitallowfullscreen="true"
        mozallowfullscreen="true"
      ></iframe>
    `}static get properties(){return{hass:Object,narrow:Boolean,panel:Object}}}customElements.define("ha-panel-iframe",n)},3426:(e,t,a)=>{a(21384);var l=a(11654);const o=document.createElement("template");o.setAttribute("style","display: none;"),o.innerHTML=`<dom-module id="ha-style">\n  <template>\n    <style>\n    ${l.Qx.cssText}\n    </style>\n  </template>\n</dom-module>`,document.head.appendChild(o.content)}}]);
//# sourceMappingURL=866e0b73.js.map