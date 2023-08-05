/*! For license information please see 5ef5289d.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[61765],{39841:function(n,t,e){e(65233),e(65660);var i,o,r,a=e(9672),s=e(87156),l=e(50856),c=e(44181);(0,a.k)({_template:(0,l.d)(i||(o=['\n    <style>\n      :host {\n        display: block;\n        /**\n         * Force app-header-layout to have its own stacking context so that its parent can\n         * control the stacking of it relative to other elements (e.g. app-drawer-layout).\n         * This could be done using `isolation: isolate`, but that\'s not well supported\n         * across browsers.\n         */\n        position: relative;\n        z-index: 0;\n      }\n\n      #wrapper ::slotted([slot=header]) {\n        @apply --layout-fixed-top;\n        z-index: 1;\n      }\n\n      #wrapper.initializing ::slotted([slot=header]) {\n        position: relative;\n      }\n\n      :host([has-scrolling-region]) {\n        height: 100%;\n      }\n\n      :host([has-scrolling-region]) #wrapper ::slotted([slot=header]) {\n        position: absolute;\n      }\n\n      :host([has-scrolling-region]) #wrapper.initializing ::slotted([slot=header]) {\n        position: relative;\n      }\n\n      :host([has-scrolling-region]) #wrapper #contentContainer {\n        @apply --layout-fit;\n        overflow-y: auto;\n        -webkit-overflow-scrolling: touch;\n      }\n\n      :host([has-scrolling-region]) #wrapper.initializing #contentContainer {\n        position: relative;\n      }\n\n      :host([fullbleed]) {\n        @apply --layout-vertical;\n        @apply --layout-fit;\n      }\n\n      :host([fullbleed]) #wrapper,\n      :host([fullbleed]) #wrapper #contentContainer {\n        @apply --layout-vertical;\n        @apply --layout-flex;\n      }\n\n      #contentContainer {\n        /* Create a stacking context here so that all children appear below the header. */\n        position: relative;\n        z-index: 0;\n      }\n\n      @media print {\n        :host([has-scrolling-region]) #wrapper #contentContainer {\n          overflow-y: visible;\n        }\n      }\n\n    </style>\n\n    <div id="wrapper" class="initializing">\n      <slot id="headerSlot" name="header"></slot>\n\n      <div id="contentContainer">\n        <slot></slot>\n      </div>\n    </div>\n'],r=['\n    <style>\n      :host {\n        display: block;\n        /**\n         * Force app-header-layout to have its own stacking context so that its parent can\n         * control the stacking of it relative to other elements (e.g. app-drawer-layout).\n         * This could be done using \\`isolation: isolate\\`, but that\'s not well supported\n         * across browsers.\n         */\n        position: relative;\n        z-index: 0;\n      }\n\n      #wrapper ::slotted([slot=header]) {\n        @apply --layout-fixed-top;\n        z-index: 1;\n      }\n\n      #wrapper.initializing ::slotted([slot=header]) {\n        position: relative;\n      }\n\n      :host([has-scrolling-region]) {\n        height: 100%;\n      }\n\n      :host([has-scrolling-region]) #wrapper ::slotted([slot=header]) {\n        position: absolute;\n      }\n\n      :host([has-scrolling-region]) #wrapper.initializing ::slotted([slot=header]) {\n        position: relative;\n      }\n\n      :host([has-scrolling-region]) #wrapper #contentContainer {\n        @apply --layout-fit;\n        overflow-y: auto;\n        -webkit-overflow-scrolling: touch;\n      }\n\n      :host([has-scrolling-region]) #wrapper.initializing #contentContainer {\n        position: relative;\n      }\n\n      :host([fullbleed]) {\n        @apply --layout-vertical;\n        @apply --layout-fit;\n      }\n\n      :host([fullbleed]) #wrapper,\n      :host([fullbleed]) #wrapper #contentContainer {\n        @apply --layout-vertical;\n        @apply --layout-flex;\n      }\n\n      #contentContainer {\n        /* Create a stacking context here so that all children appear below the header. */\n        position: relative;\n        z-index: 0;\n      }\n\n      @media print {\n        :host([has-scrolling-region]) #wrapper #contentContainer {\n          overflow-y: visible;\n        }\n      }\n\n    </style>\n\n    <div id="wrapper" class="initializing">\n      <slot id="headerSlot" name="header"></slot>\n\n      <div id="contentContainer">\n        <slot></slot>\n      </div>\n    </div>\n'],r||(r=o.slice(0)),i=Object.freeze(Object.defineProperties(o,{raw:{value:Object.freeze(r)}})))),is:"app-header-layout",behaviors:[c.Y],properties:{hasScrollingRegion:{type:Boolean,value:!1,reflectToAttribute:!0}},observers:["resetLayout(isAttached, hasScrollingRegion)"],get header(){return(0,s.vz)(this.$.headerSlot).getDistributedNodes()[0]},_updateLayoutStates:function(){var n=this.header;if(this.isAttached&&n){this.$.wrapper.classList.remove("initializing"),n.scrollTarget=this.hasScrollingRegion?this.$.contentContainer:this.ownerDocument.documentElement;var t=n.offsetHeight;this.hasScrollingRegion?(n.style.left="",n.style.right=""):requestAnimationFrame(function(){var t=this.getBoundingClientRect(),e=document.documentElement.clientWidth-t.right;n.style.left=t.left+"px",n.style.right=e+"px"}.bind(this));var e=this.$.contentContainer.style;n.fixed&&!n.condenses&&this.hasScrollingRegion?(e.marginTop=t+"px",e.paddingTop=""):(e.paddingTop=t+"px",e.marginTop="")}}})},63207:function(n,t,e){e(65660),e(15112);var i,o,r,a=e(9672),s=e(87156),l=e(50856),c=e(65233);(0,a.k)({_template:(0,l.d)(i||(o=["\n    <style>\n      :host {\n        @apply --layout-inline;\n        @apply --layout-center-center;\n        position: relative;\n\n        vertical-align: middle;\n\n        fill: var(--iron-icon-fill-color, currentcolor);\n        stroke: var(--iron-icon-stroke-color, none);\n\n        width: var(--iron-icon-width, 24px);\n        height: var(--iron-icon-height, 24px);\n        @apply --iron-icon;\n      }\n\n      :host([hidden]) {\n        display: none;\n      }\n    </style>\n"],r||(r=o.slice(0)),i=Object.freeze(Object.defineProperties(o,{raw:{value:Object.freeze(r)}})))),is:"iron-icon",properties:{icon:{type:String},theme:{type:String},src:{type:String},_meta:{value:c.XY.create("iron-meta",{type:"iconset"})}},observers:["_updateIcon(_meta, isAttached)","_updateIcon(theme, isAttached)","_srcChanged(src, isAttached)","_iconChanged(icon, isAttached)"],_DEFAULT_ICONSET:"icons",_iconChanged:function(n){var t=(n||"").split(":");this._iconName=t.pop(),this._iconsetName=t.pop()||this._DEFAULT_ICONSET,this._updateIcon()},_srcChanged:function(n){this._updateIcon()},_usesIconset:function(){return this.icon||!this.src},_updateIcon:function(){this._usesIconset()?(this._img&&this._img.parentNode&&(0,s.vz)(this.root).removeChild(this._img),""===this._iconName?this._iconset&&this._iconset.removeIcon(this):this._iconsetName&&this._meta&&(this._iconset=this._meta.byKey(this._iconsetName),this._iconset?(this._iconset.applyIcon(this,this._iconName,this.theme),this.unlisten(window,"iron-iconset-added","_updateIcon")):this.listen(window,"iron-iconset-added","_updateIcon"))):(this._iconset&&this._iconset.removeIcon(this),this._img||(this._img=document.createElement("img"),this._img.style.width="100%",this._img.style.height="100%",this._img.draggable=!1),this._img.src=this.src,(0,s.vz)(this.root).appendChild(this._img))}})},15112:function(n,t,e){e.d(t,{P:function(){return r}});e(65233);var i=e(9672);function o(n,t){for(var e=0;e<t.length;e++){var i=t[e];i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),Object.defineProperty(n,i.key,i)}}var r=function(){function n(t){!function(n,t){if(!(n instanceof t))throw new TypeError("Cannot call a class as a function")}(this,n),n[" "](t),this.type=t&&t.type||"default",this.key=t&&t.key,t&&"value"in t&&(this.value=t.value)}var t,e,i;return t=n,(e=[{key:"value",get:function(){var t=this.type,e=this.key;if(t&&e)return n.types[t]&&n.types[t][e]},set:function(t){var e=this.type,i=this.key;e&&i&&(e=n.types[e]=n.types[e]||{},null==t?delete e[i]:e[i]=t)}},{key:"list",get:function(){if(this.type){var t=n.types[this.type];return t?Object.keys(t).map((function(n){return a[this.type][n]}),this):[]}}},{key:"byKey",value:function(n){return this.key=n,this.value}}])&&o(t.prototype,e),i&&o(t,i),n}();r[" "]=function(){},r.types={};var a=r.types;(0,i.k)({is:"iron-meta",properties:{type:{type:String,value:"default"},key:{type:String},value:{type:String,notify:!0},self:{type:Boolean,observer:"_selfChanged"},__meta:{type:Boolean,computed:"__computeMeta(type, key, value)"}},hostAttributes:{hidden:!0},__computeMeta:function(n,t,e){var i=new r({type:n,key:t});return void 0!==e&&e!==i.value?i.value=e:this.value!==i.value&&(this.value=i.value),i},get list(){return this.__meta&&this.__meta.list},_selfChanged:function(n){n&&(this.value=this)},byKey:function(n){return new r({type:this.type,key:n}).value}})},21560:function(n,t,e){e.d(t,{ZH:function(){return h},MT:function(){return a},U2:function(){return l},RV:function(){return r},t8:function(){return c}});var i,o=function(){var n;return!navigator.userAgentData&&/Safari\//.test(navigator.userAgent)&&!/Chrom(e|ium)\//.test(navigator.userAgent)&&indexedDB.databases?new Promise((function(t){var e=function(){return indexedDB.databases().finally(t)};n=setInterval(e,100),e()})).finally((function(){return clearInterval(n)})):Promise.resolve()};function r(n){return new Promise((function(t,e){n.oncomplete=n.onsuccess=function(){return t(n.result)},n.onabort=n.onerror=function(){return e(n.error)}}))}function a(n,t){var e=o().then((function(){var e=indexedDB.open(n);return e.onupgradeneeded=function(){return e.result.createObjectStore(t)},r(e)}));return function(n,i){return e.then((function(e){return i(e.transaction(t,n).objectStore(t))}))}}function s(){return i||(i=a("keyval-store","keyval")),i}function l(n){var t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:s();return t("readonly",(function(t){return r(t.get(n))}))}function c(n,t){var e=arguments.length>2&&void 0!==arguments[2]?arguments[2]:s();return e("readwrite",(function(e){return e.put(t,n),r(e.transaction)}))}function h(){var n=arguments.length>0&&void 0!==arguments[0]?arguments[0]:s();return n("readwrite",(function(n){return n.clear(),r(n.transaction)}))}},47501:function(n,t,e){e.d(t,{V:function(){return i.V}});var i=e(84298)}}]);