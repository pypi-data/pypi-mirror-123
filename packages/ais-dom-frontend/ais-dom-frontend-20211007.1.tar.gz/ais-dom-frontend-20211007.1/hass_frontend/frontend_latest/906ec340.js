/*! For license information please see 906ec340.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[70357,49995,11364,70686,85143,58251,19870,1326,90739,3093],{18601:(t,e,i)=>{i.d(e,{qN:()=>r.q,Wg:()=>c});var n,o,a=i(87480),s=i(32207),r=i(78220);const l=null!==(o=null===(n=window.ShadyDOM)||void 0===n?void 0:n.inUse)&&void 0!==o&&o;class c extends r.H{constructor(){super(...arguments),this.disabled=!1,this.containingForm=null,this.formDataListener=t=>{this.disabled||this.setFormData(t.formData)}}findFormElement(){if(!this.shadowRoot||l)return null;const t=this.getRootNode().querySelectorAll("form");for(const e of Array.from(t))if(e.contains(this))return e;return null}connectedCallback(){var t;super.connectedCallback(),this.containingForm=this.findFormElement(),null===(t=this.containingForm)||void 0===t||t.addEventListener("formdata",this.formDataListener)}disconnectedCallback(){var t;super.disconnectedCallback(),null===(t=this.containingForm)||void 0===t||t.removeEventListener("formdata",this.formDataListener),this.containingForm=null}click(){this.formElement&&!this.disabled&&(this.formElement.focus(),this.formElement.click())}firstUpdated(){super.firstUpdated(),this.shadowRoot&&this.mdcRoot.addEventListener("change",(t=>{this.dispatchEvent(new Event("change",t))}))}}c.shadowRootOptions={mode:"open",delegatesFocus:!0},(0,a.__decorate)([(0,s.Cb)({type:Boolean})],c.prototype,"disabled",void 0)},14114:(t,e,i)=>{i.d(e,{P:()=>n});const n=t=>(e,i)=>{if(e.constructor._observers){if(!e.constructor.hasOwnProperty("_observers")){const t=e.constructor._observers;e.constructor._observers=new Map,t.forEach(((t,i)=>e.constructor._observers.set(i,t)))}}else{e.constructor._observers=new Map;const t=e.updated;e.updated=function(e){t.call(this,e),e.forEach(((t,e)=>{const i=this.constructor._observers.get(e);void 0!==i&&i.call(this,this[e],t)}))}}e.constructor._observers.set(i,t)}},63207:(t,e,i)=>{i(65660),i(15112);var n=i(9672),o=i(87156),a=i(50856),s=i(65233);(0,n.k)({_template:a.d`
    <style>
      :host {
        @apply --layout-inline;
        @apply --layout-center-center;
        position: relative;

        vertical-align: middle;

        fill: var(--iron-icon-fill-color, currentcolor);
        stroke: var(--iron-icon-stroke-color, none);

        width: var(--iron-icon-width, 24px);
        height: var(--iron-icon-height, 24px);
        @apply --iron-icon;
      }

      :host([hidden]) {
        display: none;
      }
    </style>
`,is:"iron-icon",properties:{icon:{type:String},theme:{type:String},src:{type:String},_meta:{value:s.XY.create("iron-meta",{type:"iconset"})}},observers:["_updateIcon(_meta, isAttached)","_updateIcon(theme, isAttached)","_srcChanged(src, isAttached)","_iconChanged(icon, isAttached)"],_DEFAULT_ICONSET:"icons",_iconChanged:function(t){var e=(t||"").split(":");this._iconName=e.pop(),this._iconsetName=e.pop()||this._DEFAULT_ICONSET,this._updateIcon()},_srcChanged:function(t){this._updateIcon()},_usesIconset:function(){return this.icon||!this.src},_updateIcon:function(){this._usesIconset()?(this._img&&this._img.parentNode&&(0,o.vz)(this.root).removeChild(this._img),""===this._iconName?this._iconset&&this._iconset.removeIcon(this):this._iconsetName&&this._meta&&(this._iconset=this._meta.byKey(this._iconsetName),this._iconset?(this._iconset.applyIcon(this,this._iconName,this.theme),this.unlisten(window,"iron-iconset-added","_updateIcon")):this.listen(window,"iron-iconset-added","_updateIcon"))):(this._iconset&&this._iconset.removeIcon(this),this._img||(this._img=document.createElement("img"),this._img.style.width="100%",this._img.style.height="100%",this._img.draggable=!1),this._img.src=this.src,(0,o.vz)(this.root).appendChild(this._img))}})},15112:(t,e,i)=>{i.d(e,{P:()=>o});i(65233);var n=i(9672);class o{constructor(t){o[" "](t),this.type=t&&t.type||"default",this.key=t&&t.key,t&&"value"in t&&(this.value=t.value)}get value(){var t=this.type,e=this.key;if(t&&e)return o.types[t]&&o.types[t][e]}set value(t){var e=this.type,i=this.key;e&&i&&(e=o.types[e]=o.types[e]||{},null==t?delete e[i]:e[i]=t)}get list(){if(this.type){var t=o.types[this.type];return t?Object.keys(t).map((function(t){return a[this.type][t]}),this):[]}}byKey(t){return this.key=t,this.value}}o[" "]=function(){},o.types={};var a=o.types;(0,n.k)({is:"iron-meta",properties:{type:{type:String,value:"default"},key:{type:String},value:{type:String,notify:!0},self:{type:Boolean,observer:"_selfChanged"},__meta:{type:Boolean,computed:"__computeMeta(type, key, value)"}},hostAttributes:{hidden:!0},__computeMeta:function(t,e,i){var n=new o({type:t,key:e});return void 0!==i&&i!==n.value?n.value=i:this.value!==n.value&&(this.value=n.value),n},get list(){return this.__meta&&this.__meta.list},_selfChanged:function(t){t&&(this.value=this)},byKey:function(t){return new o({type:this.type,key:t}).value}})},67810:(t,e,i)=>{i.d(e,{o:()=>o});i(65233);var n=i(87156);const o={properties:{scrollTarget:{type:HTMLElement,value:function(){return this._defaultScrollTarget}}},observers:["_scrollTargetChanged(scrollTarget, isAttached)"],_shouldHaveListener:!0,_scrollTargetChanged:function(t,e){if(this._oldScrollTarget&&(this._toggleScrollListener(!1,this._oldScrollTarget),this._oldScrollTarget=null),e)if("document"===t)this.scrollTarget=this._doc;else if("string"==typeof t){var i=this.domHost;this.scrollTarget=i&&i.$?i.$[t]:(0,n.vz)(this.ownerDocument).querySelector("#"+t)}else this._isValidScrollTarget()&&(this._oldScrollTarget=t,this._toggleScrollListener(this._shouldHaveListener,t))},_scrollHandler:function(){},get _defaultScrollTarget(){return this._doc},get _doc(){return this.ownerDocument.documentElement},get _scrollTop(){return this._isValidScrollTarget()?this.scrollTarget===this._doc?window.pageYOffset:this.scrollTarget.scrollTop:0},get _scrollLeft(){return this._isValidScrollTarget()?this.scrollTarget===this._doc?window.pageXOffset:this.scrollTarget.scrollLeft:0},set _scrollTop(t){this.scrollTarget===this._doc?window.scrollTo(window.pageXOffset,t):this._isValidScrollTarget()&&(this.scrollTarget.scrollTop=t)},set _scrollLeft(t){this.scrollTarget===this._doc?window.scrollTo(t,window.pageYOffset):this._isValidScrollTarget()&&(this.scrollTarget.scrollLeft=t)},scroll:function(t,e){var i;"object"==typeof t?(i=t.left,e=t.top):i=t,i=i||0,e=e||0,this.scrollTarget===this._doc?window.scrollTo(i,e):this._isValidScrollTarget()&&(this.scrollTarget.scrollLeft=i,this.scrollTarget.scrollTop=e)},get _scrollTargetWidth(){return this._isValidScrollTarget()?this.scrollTarget===this._doc?window.innerWidth:this.scrollTarget.offsetWidth:0},get _scrollTargetHeight(){return this._isValidScrollTarget()?this.scrollTarget===this._doc?window.innerHeight:this.scrollTarget.offsetHeight:0},_isValidScrollTarget:function(){return this.scrollTarget instanceof HTMLElement},_toggleScrollListener:function(t,e){var i=e===this._doc?window:e;t?this._boundScrollHandler||(this._boundScrollHandler=this._scrollHandler.bind(this),i.addEventListener("scroll",this._boundScrollHandler)):this._boundScrollHandler&&(i.removeEventListener("scroll",this._boundScrollHandler),this._boundScrollHandler=null)},toggleScrollListener:function(t){this._shouldHaveListener=t,this._toggleScrollListener(t,this.scrollTarget)}}},25782:(t,e,i)=>{i(65233),i(65660),i(70019),i(97968);var n=i(9672),o=i(50856),a=i(33760);(0,n.k)({_template:o.d`
    <style include="paper-item-shared-styles"></style>
    <style>
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
        @apply --paper-icon-item;
      }

      .content-icon {
        @apply --layout-horizontal;
        @apply --layout-center;

        width: var(--paper-item-icon-width, 56px);
        @apply --paper-item-icon;
      }
    </style>

    <div id="contentIcon" class="content-icon">
      <slot name="item-icon"></slot>
    </div>
    <slot></slot>
`,is:"paper-icon-item",behaviors:[a.U]})},33760:(t,e,i)=>{i.d(e,{U:()=>a});i(65233);var n=i(51644),o=i(26110);const a=[n.P,o.a,{hostAttributes:{role:"option",tabindex:"0"}}]},89194:(t,e,i)=>{i(65233),i(65660),i(70019);var n=i(9672),o=i(50856);(0,n.k)({_template:o.d`
    <style>
      :host {
        overflow: hidden; /* needed for text-overflow: ellipsis to work on ff */
        @apply --layout-vertical;
        @apply --layout-center-justified;
        @apply --layout-flex;
      }

      :host([two-line]) {
        min-height: var(--paper-item-body-two-line-min-height, 72px);
      }

      :host([three-line]) {
        min-height: var(--paper-item-body-three-line-min-height, 88px);
      }

      :host > ::slotted(*) {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      :host > ::slotted([secondary]) {
        @apply --paper-font-body1;

        color: var(--paper-item-body-secondary-color, var(--secondary-text-color));

        @apply --paper-item-body-secondary;
      }
    </style>

    <slot></slot>
`,is:"paper-item-body"})},97968:(t,e,i)=>{i(65660),i(70019);const n=document.createElement("template");n.setAttribute("style","display: none;"),n.innerHTML="<dom-module id=\"paper-item-shared-styles\">\n  <template>\n    <style>\n      :host, .paper-item {\n        display: block;\n        position: relative;\n        min-height: var(--paper-item-min-height, 48px);\n        padding: 0px 16px;\n      }\n\n      .paper-item {\n        @apply --paper-font-subhead;\n        border:none;\n        outline: none;\n        background: white;\n        width: 100%;\n        text-align: left;\n      }\n\n      :host([hidden]), .paper-item[hidden] {\n        display: none !important;\n      }\n\n      :host(.iron-selected), .paper-item.iron-selected {\n        font-weight: var(--paper-item-selected-weight, bold);\n\n        @apply --paper-item-selected;\n      }\n\n      :host([disabled]), .paper-item[disabled] {\n        color: var(--paper-item-disabled-color, var(--disabled-text-color));\n\n        @apply --paper-item-disabled;\n      }\n\n      :host(:focus), .paper-item:focus {\n        position: relative;\n        outline: 0;\n\n        @apply --paper-item-focused;\n      }\n\n      :host(:focus):before, .paper-item:focus:before {\n        @apply --layout-fit;\n\n        background: currentColor;\n        content: '';\n        opacity: var(--dark-divider-opacity);\n        pointer-events: none;\n\n        @apply --paper-item-focused-before;\n      }\n    </style>\n  </template>\n</dom-module>",document.head.appendChild(n.content)},53973:(t,e,i)=>{i(65233),i(65660),i(97968);var n=i(9672),o=i(50856),a=i(33760);(0,n.k)({_template:o.d`
    <style include="paper-item-shared-styles">
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
      }
    </style>
    <slot></slot>
`,is:"paper-item",behaviors:[a.U]})},51095:(t,e,i)=>{i(65233);var n=i(78161),o=i(9672),a=i(50856);(0,o.k)({_template:a.d`
    <style>
      :host {
        display: block;
        padding: 8px 0;

        background: var(--paper-listbox-background-color, var(--primary-background-color));
        color: var(--paper-listbox-color, var(--primary-text-color));

        @apply --paper-listbox;
      }
    </style>

    <slot></slot>
`,is:"paper-listbox",behaviors:[n.i],hostAttributes:{role:"listbox"}})},54444:(t,e,i)=>{i(65233);var n=i(9672),o=i(87156),a=i(50856);(0,n.k)({_template:a.d`
    <style>
      :host {
        display: block;
        position: absolute;
        outline: none;
        z-index: 1002;
        -moz-user-select: none;
        -ms-user-select: none;
        -webkit-user-select: none;
        user-select: none;
        cursor: default;
      }

      #tooltip {
        display: block;
        outline: none;
        @apply --paper-font-common-base;
        font-size: 10px;
        line-height: 1;
        background-color: var(--paper-tooltip-background, #616161);
        color: var(--paper-tooltip-text-color, white);
        padding: 8px;
        border-radius: 2px;
        @apply --paper-tooltip;
      }

      @keyframes keyFrameScaleUp {
        0% {
          transform: scale(0.0);
        }
        100% {
          transform: scale(1.0);
        }
      }

      @keyframes keyFrameScaleDown {
        0% {
          transform: scale(1.0);
        }
        100% {
          transform: scale(0.0);
        }
      }

      @keyframes keyFrameFadeInOpacity {
        0% {
          opacity: 0;
        }
        100% {
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
      }

      @keyframes keyFrameFadeOutOpacity {
        0% {
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
        100% {
          opacity: 0;
        }
      }

      @keyframes keyFrameSlideDownIn {
        0% {
          transform: translateY(-2000px);
          opacity: 0;
        }
        10% {
          opacity: 0.2;
        }
        100% {
          transform: translateY(0);
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
      }

      @keyframes keyFrameSlideDownOut {
        0% {
          transform: translateY(0);
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
        10% {
          opacity: 0.2;
        }
        100% {
          transform: translateY(-2000px);
          opacity: 0;
        }
      }

      .fade-in-animation {
        opacity: 0;
        animation-delay: var(--paper-tooltip-delay-in, 500ms);
        animation-name: keyFrameFadeInOpacity;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-in, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .fade-out-animation {
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 0ms);
        animation-name: keyFrameFadeOutOpacity;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .scale-up-animation {
        transform: scale(0);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-in, 500ms);
        animation-name: keyFrameScaleUp;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-in, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .scale-down-animation {
        transform: scale(1);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameScaleDown;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .slide-down-animation {
        transform: translateY(-2000px);
        opacity: 0;
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameSlideDownIn;
        animation-iteration-count: 1;
        animation-timing-function: cubic-bezier(0.0, 0.0, 0.2, 1);
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .slide-down-animation-out {
        transform: translateY(0);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameSlideDownOut;
        animation-iteration-count: 1;
        animation-timing-function: cubic-bezier(0.4, 0.0, 1, 1);
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .cancel-animation {
        animation-delay: -30s !important;
      }

      /* Thanks IE 10. */

      .hidden {
        display: none !important;
      }
    </style>

    <div id="tooltip" class="hidden">
      <slot></slot>
    </div>
`,is:"paper-tooltip",hostAttributes:{role:"tooltip",tabindex:-1},properties:{for:{type:String,observer:"_findTarget"},manualMode:{type:Boolean,value:!1,observer:"_manualModeChanged"},position:{type:String,value:"bottom"},fitToVisibleBounds:{type:Boolean,value:!1},offset:{type:Number,value:14},marginTop:{type:Number,value:14},animationDelay:{type:Number,value:500,observer:"_delayChange"},animationEntry:{type:String,value:""},animationExit:{type:String,value:""},animationConfig:{type:Object,value:function(){return{entry:[{name:"fade-in-animation",node:this,timing:{delay:0}}],exit:[{name:"fade-out-animation",node:this}]}}},_showing:{type:Boolean,value:!1}},listeners:{webkitAnimationEnd:"_onAnimationEnd"},get target(){var t=(0,o.vz)(this).parentNode,e=(0,o.vz)(this).getOwnerRoot();return this.for?(0,o.vz)(e).querySelector("#"+this.for):t.nodeType==Node.DOCUMENT_FRAGMENT_NODE?e.host:t},attached:function(){this._findTarget()},detached:function(){this.manualMode||this._removeListeners()},playAnimation:function(t){"entry"===t?this.show():"exit"===t&&this.hide()},cancelAnimation:function(){this.$.tooltip.classList.add("cancel-animation")},show:function(){if(!this._showing){if(""===(0,o.vz)(this).textContent.trim()){for(var t=!0,e=(0,o.vz)(this).getEffectiveChildNodes(),i=0;i<e.length;i++)if(""!==e[i].textContent.trim()){t=!1;break}if(t)return}this._showing=!0,this.$.tooltip.classList.remove("hidden"),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.updatePosition(),this._animationPlaying=!0,this.$.tooltip.classList.add(this._getAnimationType("entry"))}},hide:function(){if(this._showing){if(this._animationPlaying)return this._showing=!1,void this._cancelAnimation();this._onAnimationFinish(),this._showing=!1,this._animationPlaying=!0}},updatePosition:function(){if(this._target&&this.offsetParent){var t=this.offset;14!=this.marginTop&&14==this.offset&&(t=this.marginTop);var e,i,n=this.offsetParent.getBoundingClientRect(),o=this._target.getBoundingClientRect(),a=this.getBoundingClientRect(),s=(o.width-a.width)/2,r=(o.height-a.height)/2,l=o.left-n.left,c=o.top-n.top;switch(this.position){case"top":e=l+s,i=c-a.height-t;break;case"bottom":e=l+s,i=c+o.height+t;break;case"left":e=l-a.width-t,i=c+r;break;case"right":e=l+o.width+t,i=c+r}this.fitToVisibleBounds?(n.left+e+a.width>window.innerWidth?(this.style.right="0px",this.style.left="auto"):(this.style.left=Math.max(0,e)+"px",this.style.right="auto"),n.top+i+a.height>window.innerHeight?(this.style.bottom=n.height-c+t+"px",this.style.top="auto"):(this.style.top=Math.max(-n.top,i)+"px",this.style.bottom="auto")):(this.style.left=e+"px",this.style.top=i+"px")}},_addListeners:function(){this._target&&(this.listen(this._target,"mouseenter","show"),this.listen(this._target,"focus","show"),this.listen(this._target,"mouseleave","hide"),this.listen(this._target,"blur","hide"),this.listen(this._target,"tap","hide")),this.listen(this.$.tooltip,"animationend","_onAnimationEnd"),this.listen(this,"mouseenter","hide")},_findTarget:function(){this.manualMode||this._removeListeners(),this._target=this.target,this.manualMode||this._addListeners()},_delayChange:function(t){500!==t&&this.updateStyles({"--paper-tooltip-delay-in":t+"ms"})},_manualModeChanged:function(){this.manualMode?this._removeListeners():this._addListeners()},_cancelAnimation:function(){this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add("hidden")},_onAnimationFinish:function(){this._showing&&(this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add(this._getAnimationType("exit")))},_onAnimationEnd:function(){this._animationPlaying=!1,this._showing||(this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.add("hidden"))},_getAnimationType:function(t){if("entry"===t&&""!==this.animationEntry)return this.animationEntry;if("exit"===t&&""!==this.animationExit)return this.animationExit;if(this.animationConfig[t]&&"string"==typeof this.animationConfig[t][0].name){if(this.animationConfig[t][0].timing&&this.animationConfig[t][0].timing.delay&&0!==this.animationConfig[t][0].timing.delay){var e=this.animationConfig[t][0].timing.delay;"entry"===t?this.updateStyles({"--paper-tooltip-delay-in":e+"ms"}):"exit"===t&&this.updateStyles({"--paper-tooltip-delay-out":e+"ms"})}return this.animationConfig[t][0].name}},_removeListeners:function(){this._target&&(this.unlisten(this._target,"mouseenter","show"),this.unlisten(this._target,"focus","show"),this.unlisten(this._target,"mouseleave","hide"),this.unlisten(this._target,"blur","hide"),this.unlisten(this._target,"tap","hide")),this.unlisten(this.$.tooltip,"animationend","_onAnimationEnd"),this.unlisten(this,"mouseenter","hide")}})},3239:(t,e,i)=>{function n(t){if(!t||"object"!=typeof t)return t;if("[object Date]"==Object.prototype.toString.call(t))return new Date(t.getTime());if(Array.isArray(t))return t.map(n);var e={};return Object.keys(t).forEach((function(i){e[i]=n(t[i])})),e}i.d(e,{Z:()=>n})},21560:(t,e,i)=>{i.d(e,{ZH:()=>p,MT:()=>a,U2:()=>l,RV:()=>o,t8:()=>c});const n=function(){if(!(!navigator.userAgentData&&/Safari\//.test(navigator.userAgent)&&!/Chrom(e|ium)\//.test(navigator.userAgent))||!indexedDB.databases)return Promise.resolve();let t;return new Promise((e=>{const i=()=>indexedDB.databases().finally(e);t=setInterval(i,100),i()})).finally((()=>clearInterval(t)))};function o(t){return new Promise(((e,i)=>{t.oncomplete=t.onsuccess=()=>e(t.result),t.onabort=t.onerror=()=>i(t.error)}))}function a(t,e){const i=n().then((()=>{const i=indexedDB.open(t);return i.onupgradeneeded=()=>i.result.createObjectStore(e),o(i)}));return(t,n)=>i.then((i=>n(i.transaction(e,t).objectStore(e))))}let s;function r(){return s||(s=a("keyval-store","keyval")),s}function l(t,e=r()){return e("readonly",(e=>o(e.get(t))))}function c(t,e,i=r()){return i("readwrite",(i=>(i.put(e,t),o(i.transaction))))}function p(t=r()){return t("readwrite",(t=>(t.clear(),o(t.transaction))))}},93217:(t,e,i)=>{i.d(e,{Ud:()=>h});const n=Symbol("Comlink.proxy"),o=Symbol("Comlink.endpoint"),a=Symbol("Comlink.releaseProxy"),s=Symbol("Comlink.thrown"),r=t=>"object"==typeof t&&null!==t||"function"==typeof t,l=new Map([["proxy",{canHandle:t=>r(t)&&t[n],serialize(t){const{port1:e,port2:i}=new MessageChannel;return c(t,e),[i,[i]]},deserialize:t=>(t.start(),h(t))}],["throw",{canHandle:t=>r(t)&&s in t,serialize({value:t}){let e;return e=t instanceof Error?{isError:!0,value:{message:t.message,name:t.name,stack:t.stack}}:{isError:!1,value:t},[e,[]]},deserialize(t){if(t.isError)throw Object.assign(new Error(t.value.message),t.value);throw t.value}}]]);function c(t,e=self){e.addEventListener("message",(function i(o){if(!o||!o.data)return;const{id:a,type:r,path:l}=Object.assign({path:[]},o.data),h=(o.data.argumentList||[]).map(g);let d;try{const e=l.slice(0,-1).reduce(((t,e)=>t[e]),t),i=l.reduce(((t,e)=>t[e]),t);switch(r){case"GET":d=i;break;case"SET":e[l.slice(-1)[0]]=g(o.data.value),d=!0;break;case"APPLY":d=i.apply(e,h);break;case"CONSTRUCT":d=function(t){return Object.assign(t,{[n]:!0})}(new i(...h));break;case"ENDPOINT":{const{port1:e,port2:i}=new MessageChannel;c(t,i),d=function(t,e){return y.set(t,e),t}(e,[e])}break;case"RELEASE":d=void 0;break;default:return}}catch(t){d={value:t,[s]:0}}Promise.resolve(d).catch((t=>({value:t,[s]:0}))).then((t=>{const[n,o]=f(t);e.postMessage(Object.assign(Object.assign({},n),{id:a}),o),"RELEASE"===r&&(e.removeEventListener("message",i),p(e))}))})),e.start&&e.start()}function p(t){(function(t){return"MessagePort"===t.constructor.name})(t)&&t.close()}function h(t,e){return u(t,[],e)}function d(t){if(t)throw new Error("Proxy has been released and is not useable")}function u(t,e=[],i=function(){}){let n=!1;const s=new Proxy(i,{get(i,o){if(d(n),o===a)return()=>v(t,{type:"RELEASE",path:e.map((t=>t.toString()))}).then((()=>{p(t),n=!0}));if("then"===o){if(0===e.length)return{then:()=>s};const i=v(t,{type:"GET",path:e.map((t=>t.toString()))}).then(g);return i.then.bind(i)}return u(t,[...e,o])},set(i,o,a){d(n);const[s,r]=f(a);return v(t,{type:"SET",path:[...e,o].map((t=>t.toString())),value:s},r).then(g)},apply(i,a,s){d(n);const r=e[e.length-1];if(r===o)return v(t,{type:"ENDPOINT"}).then(g);if("bind"===r)return u(t,e.slice(0,-1));const[l,c]=m(s);return v(t,{type:"APPLY",path:e.map((t=>t.toString())),argumentList:l},c).then(g)},construct(i,o){d(n);const[a,s]=m(o);return v(t,{type:"CONSTRUCT",path:e.map((t=>t.toString())),argumentList:a},s).then(g)}});return s}function m(t){const e=t.map(f);return[e.map((t=>t[0])),(i=e.map((t=>t[1])),Array.prototype.concat.apply([],i))];var i}const y=new WeakMap;function f(t){for(const[e,i]of l)if(i.canHandle(t)){const[n,o]=i.serialize(t);return[{type:"HANDLER",name:e,value:n},o]}return[{type:"RAW",value:t},y.get(t)||[]]}function g(t){switch(t.type){case"HANDLER":return l.get(t.name).deserialize(t.value);case"RAW":return t.value}}function v(t,e,i){return new Promise((n=>{const o=new Array(4).fill(0).map((()=>Math.floor(Math.random()*Number.MAX_SAFE_INTEGER).toString(16))).join("-");t.addEventListener("message",(function e(i){i.data&&i.data.id&&i.data.id===o&&(t.removeEventListener("message",e),n(i.data))})),t.start&&t.start(),t.postMessage(Object.assign({id:o},e),i)}))}},19596:(t,e,i)=>{i.d(e,{s:()=>h});var n=i(81563),o=i(38941);const a=(t,e)=>{var i,n;const o=t._$AN;if(void 0===o)return!1;for(const t of o)null===(n=(i=t)._$AO)||void 0===n||n.call(i,e,!1),a(t,e);return!0},s=t=>{let e,i;do{if(void 0===(e=t._$AM))break;i=e._$AN,i.delete(t),t=e}while(0===(null==i?void 0:i.size))},r=t=>{for(let e;e=t._$AM;t=e){let i=e._$AN;if(void 0===i)e._$AN=i=new Set;else if(i.has(t))break;i.add(t),p(e)}};function l(t){void 0!==this._$AN?(s(this),this._$AM=t,r(this)):this._$AM=t}function c(t,e=!1,i=0){const n=this._$AH,o=this._$AN;if(void 0!==o&&0!==o.size)if(e)if(Array.isArray(n))for(let t=i;t<n.length;t++)a(n[t],!1),s(n[t]);else null!=n&&(a(n,!1),s(n));else a(this,t)}const p=t=>{var e,i,n,a;t.type==o.pX.CHILD&&(null!==(e=(n=t)._$AP)&&void 0!==e||(n._$AP=c),null!==(i=(a=t)._$AQ)&&void 0!==i||(a._$AQ=l))};class h extends o.Xe{constructor(){super(...arguments),this._$AN=void 0}_$AT(t,e,i){super._$AT(t,e,i),r(this),this.isConnected=t._$AU}_$AO(t,e=!0){var i,n;t!==this.isConnected&&(this.isConnected=t,t?null===(i=this.reconnected)||void 0===i||i.call(this):null===(n=this.disconnected)||void 0===n||n.call(this)),e&&(a(this,t),s(this))}setValue(t){if((0,n.OR)(this._$Ct))this._$Ct._$AI(t,this);else{const e=[...this._$Ct._$AH];e[this._$Ci]=t,this._$Ct._$AI(e,this,0)}}disconnected(){}reconnected(){}}},81563:(t,e,i)=>{i.d(e,{E_:()=>y,i9:()=>u,_Y:()=>c,pt:()=>a,OR:()=>r,hN:()=>s,ws:()=>m,fk:()=>p,hl:()=>d});var n=i(15304);const{H:o}=n.Al,a=t=>null===t||"object"!=typeof t&&"function"!=typeof t,s=(t,e)=>{var i,n;return void 0===e?void 0!==(null===(i=t)||void 0===i?void 0:i._$litType$):(null===(n=t)||void 0===n?void 0:n._$litType$)===e},r=t=>void 0===t.strings,l=()=>document.createComment(""),c=(t,e,i)=>{var n;const a=t._$AA.parentNode,s=void 0===e?t._$AB:e._$AA;if(void 0===i){const e=a.insertBefore(l(),s),n=a.insertBefore(l(),s);i=new o(e,n,t,t.options)}else{const e=i._$AB.nextSibling,o=i._$AM,r=o!==t;if(r){let e;null===(n=i._$AQ)||void 0===n||n.call(i,t),i._$AM=t,void 0!==i._$AP&&(e=t._$AU)!==o._$AU&&i._$AP(e)}if(e!==s||r){let t=i._$AA;for(;t!==e;){const e=t.nextSibling;a.insertBefore(t,s),t=e}}}return i},p=(t,e,i=t)=>(t._$AI(e,i),t),h={},d=(t,e=h)=>t._$AH=e,u=t=>t._$AH,m=t=>{var e;null===(e=t._$AP)||void 0===e||e.call(t,!1,!0);let i=t._$AA;const n=t._$AB.nextSibling;for(;i!==n;){const t=i.nextSibling;i.remove(),i=t}},y=t=>{t._$AR()}},57835:(t,e,i)=>{i.d(e,{Xe:()=>n.Xe,pX:()=>n.pX,XM:()=>n.XM});var n=i(38941)},228:(t,e,i)=>{i.d(e,{$:()=>n.$});var n=i(59685)},48399:(t,e,i)=>{i.d(e,{o:()=>n.o});var n=i(88668)},47501:(t,e,i)=>{i.d(e,{V:()=>n.V});var n=i(84298)}}]);
//# sourceMappingURL=906ec340.js.map