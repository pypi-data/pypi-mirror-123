"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[57673],{44583:(e,t,r)=>{r.a(e,(async e=>{r.d(t,{o0:()=>s,E8:()=>l});var i=r(14516),o=r(65810),n=r(91177);n.Xp&&await n.Xp;const s=(e,t)=>a(t).format(e),a=(0,i.Z)((e=>new Intl.DateTimeFormat(e.language,{year:"numeric",month:"long",day:"numeric",hour:(0,o.y)(e)?"numeric":"2-digit",minute:"2-digit",hour12:(0,o.y)(e)}))),l=(e,t)=>c(t).format(e),c=(0,i.Z)((e=>new Intl.DateTimeFormat(e.language,{year:"numeric",month:"long",day:"numeric",hour:(0,o.y)(e)?"numeric":"2-digit",minute:"2-digit",second:"2-digit",hour12:(0,o.y)(e)})));(0,i.Z)((e=>new Intl.DateTimeFormat(e.language,{year:"numeric",month:"numeric",day:"numeric",hour:"numeric",minute:"2-digit",hour12:(0,o.y)(e)})));e()}),1)},65810:(e,t,r)=>{r.d(t,{y:()=>n});var i=r(14516),o=r(66477);const n=(0,i.Z)((e=>{if(e.time_format===o.zt.language||e.time_format===o.zt.system){const t=e.time_format===o.zt.language?e.language:void 0,r=(new Date).toLocaleString(t);return r.includes("AM")||r.includes("PM")}return e.time_format===o.zt.am_pm}))},25516:(e,t,r)=>{r.d(t,{i:()=>i});const i=e=>t=>({kind:"method",placement:"prototype",key:t.key,descriptor:{set(e){this[`__${String(t.key)}`]=e},get(){return this[`__${String(t.key)}`]},enumerable:!0,configurable:!0},finisher(r){const i=r.prototype.connectedCallback;r.prototype.connectedCallback=function(){if(i.call(this),this[t.key]){const r=this.renderRoot.querySelector(e);if(!r)return;r.scrollTop=this[t.key]}}}})},85415:(e,t,r)=>{r.d(t,{$:()=>i,f:()=>o});const i=(e,t)=>e<t?-1:e>t?1:0,o=(e,t)=>i(e.toLowerCase(),t.toLowerCase())},98762:(e,t,r)=>{r(53918);var i=r(7599),o=r(26767),n=r(5701),s=r(67352);r(31206);function a(){a=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:r;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!d(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return h(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?h(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=f(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:p(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=p(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function l(e){var t,r=f(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function c(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function d(e){return e.decorators&&e.decorators.length}function u(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function p(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function f(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function h(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}!function(e,t,r,i){var o=a();if(i)for(var n=0;n<i.length;n++)o=i[n](o);var s=t((function(e){o.initializeInstanceElements(e,p.elements)}),r),p=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var o,n=e[i];if("method"===n.kind&&(o=t.find(r)))if(u(n.descriptor)||u(o.descriptor)){if(d(n)||d(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(d(n)){if(d(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}c(n,o)}else t.push(n)}return t}(s.d.map(l)),e);o.initializeClassElements(s.F,p.elements),o.runClassFinishers(s.F,p.finishers)}([(0,o.M)("ha-progress-button")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.C)({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[(0,n.C)({type:Boolean})],key:"progress",value:()=>!1},{kind:"field",decorators:[(0,n.C)({type:Boolean})],key:"raised",value:()=>!1},{kind:"field",decorators:[(0,s.I)("mwc-button",!0)],key:"_button",value:void 0},{kind:"method",key:"render",value:function(){return i.dy`
      <mwc-button
        ?raised=${this.raised}
        .disabled=${this.disabled||this.progress}
        @click=${this._buttonTapped}
      >
        <slot></slot>
      </mwc-button>
      ${this.progress?i.dy`<div class="progress">
            <ha-circular-progress size="small" active></ha-circular-progress>
          </div>`:""}
    `}},{kind:"method",key:"actionSuccess",value:function(){this._tempClass("success")}},{kind:"method",key:"actionError",value:function(){this._tempClass("error")}},{kind:"method",key:"_tempClass",value:function(e){this._button.classList.add(e),setTimeout((()=>{this._button.classList.remove(e)}),1e3)}},{kind:"method",key:"_buttonTapped",value:function(e){this.progress&&e.stopPropagation()}},{kind:"get",static:!0,key:"styles",value:function(){return i.iv`
      :host {
        outline: none;
        display: inline-block;
        position: relative;
      }

      mwc-button {
        transition: all 1s;
      }

      mwc-button.success {
        --mdc-theme-primary: white;
        background-color: var(--success-color);
        transition: none;
      }

      mwc-button[raised].success {
        --mdc-theme-primary: var(--success-color);
        --mdc-theme-on-primary: white;
      }

      mwc-button.error {
        --mdc-theme-primary: white;
        background-color: var(--error-color);
        transition: none;
      }

      mwc-button[raised].error {
        --mdc-theme-primary: var(--error-color);
        --mdc-theme-on-primary: white;
      }

      .progress {
        bottom: 0;
        margin-top: 4px;
        position: absolute;
        text-align: center;
        top: 0;
        width: 100%;
      }
    `}}]}}),i.oi)},9381:(e,t,r)=>{r(53918),r(25230);var i=r(7599),o=r(26767),n=r(5701),s=r(228),a=r(47181);r(52039);function l(){l=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:r;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!u(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return m(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?m(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=h(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:f(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=f(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function c(e){var t,r=h(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function d(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function u(e){return e.decorators&&e.decorators.length}function p(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function f(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function h(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function m(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}const y={info:"M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z",warning:"M12,2L1,21H23M12,6L19.53,19H4.47M11,10V14H13V10M11,16V18H13V16",error:"M11,15H13V17H11V15M11,7H13V13H11V7M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20Z",success:"M20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4C12.76,4 13.5,4.11 14.2,4.31L15.77,2.74C14.61,2.26 13.34,2 12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12M7.91,10.08L6.5,11.5L11,16L21,6L19.59,4.58L11,13.17L7.91,10.08Z"};!function(e,t,r,i){var o=l();if(i)for(var n=0;n<i.length;n++)o=i[n](o);var s=t((function(e){o.initializeInstanceElements(e,a.elements)}),r),a=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var o,n=e[i];if("method"===n.kind&&(o=t.find(r)))if(p(n.descriptor)||p(o.descriptor)){if(u(n)||u(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(u(n)){if(u(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}d(n,o)}else t.push(n)}return t}(s.d.map(c)),e);o.initializeClassElements(s.F,a.elements),o.runClassFinishers(s.F,a.finishers)}([(0,o.M)("ha-alert")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.C)()],key:"title",value:()=>""},{kind:"field",decorators:[(0,n.C)({attribute:"alert-type"})],key:"alertType",value:()=>"info"},{kind:"field",decorators:[(0,n.C)({attribute:"action-text"})],key:"actionText",value:()=>""},{kind:"field",decorators:[(0,n.C)({type:Boolean})],key:"dismissable",value:()=>!1},{kind:"field",decorators:[(0,n.C)({type:Boolean})],key:"rtl",value:()=>!1},{kind:"method",key:"render",value:function(){return i.dy`
      <div
        class="issue-type ${(0,s.$)({rtl:this.rtl,[this.alertType]:!0})}"
      >
        <div class="icon ${this.title?"":"no-title"}">
          <ha-svg-icon .path=${y[this.alertType]}></ha-svg-icon>
        </div>
        <div class="content">
          <div class="main-content">
            ${this.title?i.dy`<div class="title">${this.title}</div>`:""}
            <slot></slot>
          </div>
          <div class="action">
            ${this.actionText?i.dy`<mwc-button
                  @click=${this._action_clicked}
                  .label=${this.actionText}
                ></mwc-button>`:this.dismissable?i.dy`<mwc-icon-button
                  @click=${this._dismiss_clicked}
                  aria-label="Dismiss alert"
                >
                  <ha-svg-icon .path=${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}> </ha-svg-icon>
                </mwc-icon-button> `:""}
          </div>
        </div>
      </div>
    `}},{kind:"method",key:"_dismiss_clicked",value:function(){(0,a.B)(this,"alert-dismissed-clicked")}},{kind:"method",key:"_action_clicked",value:function(){(0,a.B)(this,"alert-action-clicked")}},{kind:"field",static:!0,key:"styles",value:()=>i.iv`
    .issue-type {
      position: relative;
      padding: 8px;
      display: flex;
      margin: 4px 0;
    }
    .issue-type.rtl {
      flex-direction: row-reverse;
    }
    .issue-type::before {
      position: absolute;
      top: 0;
      right: 0;
      bottom: 0;
      left: 0;
      opacity: 0.12;
      pointer-events: none;
      content: "";
      border-radius: 4px;
    }
    .icon {
      margin-right: 8px;
      width: 24px;
    }
    .icon.no-title {
      align-self: center;
    }
    .issue-type.rtl > .icon {
      margin-right: 0px;
      margin-left: 8px;
      width: 24px;
    }
    .issue-type.rtl > .content {
      flex-direction: row-reverse;
      text-align: right;
    }
    .content {
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 100%;
    }
    .main-content {
      overflow-wrap: anywhere;
    }
    .title {
      margin-top: 2px;
      font-weight: bold;
    }
    mwc-button {
      --mdc-theme-primary: var(--primary-text-color);
    }
    mwc-icon-button {
      --mdc-icon-button-size: 36px;
    }
    .issue-type.info > .icon {
      color: var(--info-color);
    }
    .issue-type.info::before {
      background-color: var(--info-color);
    }

    .issue-type.warning > .icon {
      color: var(--warning-color);
    }
    .issue-type.warning::before {
      background-color: var(--warning-color);
    }

    .issue-type.error > .icon {
      color: var(--error-color);
    }
    .issue-type.error::before {
      background-color: var(--error-color);
    }

    .issue-type.success > .icon {
      color: var(--success-color);
    }
    .issue-type.success::before {
      background-color: var(--success-color);
    }
  `}]}}),i.oi)},99282:(e,t,r)=>{var i=r(52039);class o extends i.C{connectedCallback(){super.connectedCallback(),setTimeout((()=>{this.path="ltr"===window.getComputedStyle(this).direction?"M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z":"M15.41,16.58L10.83,12L15.41,7.41L14,6L8,12L14,18L15.41,16.58Z"}),100)}}customElements.define("ha-icon-next",o)},14089:(e,t,r)=>{r(89194);var i=r(7599),o=r(26767),n=r(5701);function s(){s=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:r;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!c(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return f(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?f(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=p(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:u(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=u(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function a(e){var t,r=p(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function l(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function c(e){return e.decorators&&e.decorators.length}function d(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function u(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function p(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function f(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}!function(e,t,r,i){var o=s();if(i)for(var n=0;n<i.length;n++)o=i[n](o);var u=t((function(e){o.initializeInstanceElements(e,p.elements)}),r),p=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var o,n=e[i];if("method"===n.kind&&(o=t.find(r)))if(d(n.descriptor)||d(o.descriptor)){if(c(n)||c(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(c(n)){if(c(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}l(n,o)}else t.push(n)}return t}(u.d.map(a)),e);o.initializeClassElements(u.F,p.elements),o.runClassFinishers(u.F,p.finishers)}([(0,o.M)("ha-settings-row")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.C)({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,n.C)({type:Boolean,attribute:"three-line"})],key:"threeLine",value:()=>!1},{kind:"method",key:"render",value:function(){return i.dy`
      <div class="prefix-wrap">
        <slot name="prefix"></slot>
        <paper-item-body
          ?two-line=${!this.threeLine}
          ?three-line=${this.threeLine}
        >
          <slot name="heading"></slot>
          <div secondary><slot name="description"></slot></div>
        </paper-item-body>
      </div>
      <slot></slot>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return i.iv`
      :host {
        display: flex;
        padding: 0 16px;
        align-content: normal;
        align-self: auto;
        align-items: center;
      }
      paper-item-body {
        padding: 8px 16px 8px 0;
      }
      paper-item-body[two-line] {
        min-height: calc(
          var(--paper-item-body-two-line-min-height, 72px) - 16px
        );
        flex: 1;
      }
      :host([narrow]) {
        align-items: normal;
        flex-direction: column;
        border-top: 1px solid var(--divider-color);
        padding-bottom: 8px;
      }
      ::slotted(ha-switch) {
        padding: 16px 0;
      }
      div[secondary] {
        white-space: normal;
      }
      .prefix-wrap {
        display: contents;
      }
      :host([narrow]) .prefix-wrap {
        display: flex;
        align-items: center;
      }
    `}}]}}),i.oi)},43709:(e,t,r)=>{var i=r(32421),o=r(7599),n=r(26767),s=r(5701),a=r(62359);function l(){l=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:r;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!u(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return m(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?m(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=h(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:f(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=f(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function c(e){var t,r=h(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function d(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function u(e){return e.decorators&&e.decorators.length}function p(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function f(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function h(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function m(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function y(e,t,r){return y="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=v(e)););return e}(e,t);if(i){var o=Object.getOwnPropertyDescriptor(i,t);return o.get?o.get.call(r):o.value}},y(e,t,r||e)}function v(e){return v=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},v(e)}!function(e,t,r,i){var o=l();if(i)for(var n=0;n<i.length;n++)o=i[n](o);var s=t((function(e){o.initializeInstanceElements(e,a.elements)}),r),a=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var o,n=e[i];if("method"===n.kind&&(o=t.find(r)))if(p(n.descriptor)||p(o.descriptor)){if(u(n)||u(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(u(n)){if(u(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}d(n,o)}else t.push(n)}return t}(s.d.map(c)),e);o.initializeClassElements(s.F,a.elements),o.runClassFinishers(s.F,a.finishers)}([(0,n.M)("ha-switch")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[(0,s.C)({type:Boolean})],key:"haptic",value:()=>!1},{kind:"method",key:"firstUpdated",value:function(){y(v(r.prototype),"firstUpdated",this).call(this),this.style.setProperty("--mdc-theme-secondary","var(--switch-checked-color)"),this.addEventListener("change",(()=>{this.haptic&&(0,a.j)("light")}))}},{kind:"get",static:!0,key:"styles",value:function(){return[i.r.styles,o.iv`
        .mdc-switch.mdc-switch--checked .mdc-switch__thumb {
          background-color: var(--switch-checked-button-color);
          border-color: var(--switch-checked-button-color);
        }
        .mdc-switch.mdc-switch--checked .mdc-switch__track {
          background-color: var(--switch-checked-track-color);
          border-color: var(--switch-checked-track-color);
        }
        .mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb {
          background-color: var(--switch-unchecked-button-color);
          border-color: var(--switch-unchecked-button-color);
        }
        .mdc-switch:not(.mdc-switch--checked) .mdc-switch__track {
          background-color: var(--switch-unchecked-track-color);
          border-color: var(--switch-unchecked-track-color);
        }
      `]}}]}}),i.r)},27434:(e,t,r)=>{r.d(t,{t:()=>i,z:()=>o});const i=e=>e.callWS({type:"cloud/alexa/entities"}),o=e=>e.callWS({type:"cloud/alexa/sync"})},43408:(e,t,r)=>{r.d(t,{H:()=>i});const i=e=>e.callWS({type:"webhook/list"})},60010:(e,t,r)=>{var i=r(7599),o=r(26767),n=r(5701),s=r(84982),a=r(25516);r(2315),r(48932);function l(){l=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:r;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!u(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return m(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?m(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=h(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:f(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=f(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function c(e){var t,r=h(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function d(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function u(e){return e.decorators&&e.decorators.length}function p(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function f(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function h(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function m(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}!function(e,t,r,i){var o=l();if(i)for(var n=0;n<i.length;n++)o=i[n](o);var s=t((function(e){o.initializeInstanceElements(e,a.elements)}),r),a=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var o,n=e[i];if("method"===n.kind&&(o=t.find(r)))if(p(n.descriptor)||p(o.descriptor)){if(u(n)||u(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(u(n)){if(u(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}d(n,o)}else t.push(n)}return t}(s.d.map(c)),e);o.initializeClassElements(s.F,a.elements),o.runClassFinishers(s.F,a.finishers)}([(0,o.M)("hass-subpage")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.C)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.C)()],key:"header",value:void 0},{kind:"field",decorators:[(0,n.C)({type:Boolean,attribute:"main-page"})],key:"mainPage",value:()=>!1},{kind:"field",decorators:[(0,n.C)({type:Boolean,reflect:!0})],key:"narrow",value:()=>!1},{kind:"field",decorators:[(0,n.C)({type:Boolean})],key:"supervisor",value:()=>!1},{kind:"field",decorators:[(0,a.i)(".content")],key:"_savedScrollPos",value:void 0},{kind:"method",key:"render",value:function(){var e;return i.dy`
      <div class="toolbar">
        ${this.mainPage||null!==(e=history.state)&&void 0!==e&&e.root?i.dy`
              <ha-menu-button
                .hassio=${this.supervisor}
                .hass=${this.hass}
                .narrow=${this.narrow}
              ></ha-menu-button>
            `:i.dy`
              <ha-icon-button-arrow-prev
                .hass=${this.hass}
                @click=${this._backTapped}
              ></ha-icon-button-arrow-prev>
            `}

        <div class="main-title">${this.header}</div>
        <slot name="toolbar-icon"></slot>
      </div>
      <div class="content" @scroll=${this._saveScrollPos}><slot></slot></div>
    `}},{kind:"method",decorators:[(0,s.h)({passive:!0})],key:"_saveScrollPos",value:function(e){this._savedScrollPos=e.target.scrollTop}},{kind:"method",key:"_backTapped",value:function(){history.back()}},{kind:"get",static:!0,key:"styles",value:function(){return i.iv`
      :host {
        display: block;
        height: 100%;
        background-color: var(--primary-background-color);
      }

      :host([narrow]) {
        width: 100%;
        position: fixed;
      }

      .toolbar {
        display: flex;
        align-items: center;
        font-size: 20px;
        height: var(--header-height);
        padding: 0 16px;
        pointer-events: none;
        background-color: var(--app-header-background-color);
        font-weight: 400;
        color: var(--app-header-text-color, white);
        border-bottom: var(--app-header-border-bottom, none);
        box-sizing: border-box;
      }

      ha-menu-button,
      ha-icon-button-arrow-prev,
      ::slotted([slot="toolbar-icon"]) {
        pointer-events: auto;
      }

      .main-title {
        margin: 0 0 0 24px;
        line-height: 20px;
        flex-grow: 1;
      }

      .content {
        position: relative;
        width: 100%;
        height: calc(100% - 1px - var(--header-height));
        overflow-y: auto;
        overflow: auto;
        -webkit-overflow-scrolling: touch;
      }
    `}}]}}),i.oi)},11052:(e,t,r)=>{r.d(t,{I:()=>n});var i=r(76389),o=r(47181);const n=(0,i.o)((e=>class extends e{fire(e,t,r){return r=r||{},(0,o.B)(r.node||this,e,t,r)}}))},1265:(e,t,r)=>{r.d(t,{Z:()=>i});const i=(0,r(76389).o)((e=>class extends e{static get properties(){return{hass:Object,localize:{type:Function,computed:"__computeLocalize(hass.localize)"}}}__computeLocalize(e){return e}}))},63685:(e,t,r)=>{r.a(e,(async e=>{r(53918),r(89194);var t=r(50856),i=r(28426),o=r(44583),n=r(87744),s=(r(94132),r(22098),r(83270)),a=(r(60010),r(11052)),l=r(1265),c=(r(3426),r(88165),r(14788),r(56969),r(96112),r(84095),r(6163),e([o]));o=(c.then?await c:c)[0];class d extends((0,a.I)((0,l.Z)(i.H3))){static get template(){return t.d`
      <style include="iron-flex ha-style">
        [slot="introduction"] {
          margin: -1em 0;
        }
        [slot="introduction"] a {
          color: var(--primary-color);
        }
        .content {
          padding-bottom: 24px;
        }
        .account-row {
          display: flex;
          padding: 0 16px;
        }
        mwc-button {
          align-self: center;
        }
        .soon {
          font-style: italic;
          margin-top: 24px;
          text-align: center;
        }
        .nowrap {
          white-space: nowrap;
        }
        .wrap {
          white-space: normal;
        }
        .status {
          text-transform: capitalize;
          padding: 16px;
        }
        a {
          color: var(--primary-color);
        }
      </style>
      <hass-subpage
        hass="[[hass]]"
        narrow="[[narrow]]"
        header="Home Assistant Cloud"
      >
        <div class="content">
          <ha-config-section is-wide="[[isWide]]">
            <span slot="header">Home Assistant Cloud</span>
            <div slot="introduction">
              <p>
                [[localize('ui.panel.config.cloud.account.thank_you_note')]]
              </p>
            </div>

            <ha-card
              header="[[localize('ui.panel.config.cloud.account.nabu_casa_account')]]"
            >
              <div class="account-row">
                <paper-item-body two-line="">
                  [[cloudStatus.email]]
                  <div secondary class="wrap">
                    [[_formatSubscription(_subscription)]]
                  </div>
                </paper-item-body>
              </div>

              <div class="account-row">
                <paper-item-body
                  >[[localize('ui.panel.config.cloud.account.connection_status')]]</paper-item-body
                >
                <div class="status">
                  [[_computeConnectionStatus(cloudStatus.cloud)]]
                </div>
              </div>

              <div class="card-actions">
                <a
                  href="https://account.nabucasa.com"
                  target="_blank"
                  rel="noreferrer"
                >
                  <mwc-button
                    >[[localize('ui.panel.config.cloud.account.manage_account')]]</mwc-button
                  >
                </a>
                <mwc-button style="float: right" on-click="handleLogout"
                  >[[localize('ui.panel.config.cloud.account.sign_out')]]</mwc-button
                >
              </div>
            </ha-card>
          </ha-config-section>

          <ha-config-section is-wide="[[isWide]]">
            <span slot="header"
              >[[localize('ui.panel.config.cloud.account.integrations')]]</span
            >
            <div slot="introduction">
              <p>
                [[localize('ui.panel.config.cloud.account.integrations_introduction')]]
              </p>
              <p>
                [[localize('ui.panel.config.cloud.account.integrations_introduction2')]]
                <a
                  href="https://www.nabucasa.com"
                  target="_blank"
                  rel="noreferrer"
                >
                  [[localize('ui.panel.config.cloud.account.integrations_link_all_features')]]</a
                >.
              </p>
            </div>

            <cloud-remote-pref
              hass="[[hass]]"
              cloud-status="[[cloudStatus]]"
              dir="[[_rtlDirection]]"
            ></cloud-remote-pref>

            <cloud-tts-pref
              hass="[[hass]]"
              cloud-status="[[cloudStatus]]"
              dir="[[_rtlDirection]]"
            ></cloud-tts-pref>

            <cloud-alexa-pref
              hass="[[hass]]"
              cloud-status="[[cloudStatus]]"
              dir="[[_rtlDirection]]"
            ></cloud-alexa-pref>

            <cloud-google-pref
              hass="[[hass]]"
              cloud-status="[[cloudStatus]]"
              dir="[[_rtlDirection]]"
            ></cloud-google-pref>

            <cloud-webhooks
              hass="[[hass]]"
              cloud-status="[[cloudStatus]]"
              dir="[[_rtlDirection]]"
            ></cloud-webhooks>
          </ha-config-section>
        </div>
      </hass-subpage>
    `}static get properties(){return{hass:Object,isWide:Boolean,narrow:Boolean,cloudStatus:Object,_subscription:{type:Object,value:null},_rtlDirection:{type:Boolean,computed:"_computeRTLDirection(hass)"}}}ready(){super.ready(),this._fetchSubscriptionInfo()}_computeConnectionStatus(e){return"connected"===e?this.hass.localize("ui.panel.config.cloud.account.connected"):"disconnected"===e?this.hass.localize("ui.panel.config.cloud.account.not_connected"):this.hass.localize("ui.panel.config.cloud.account.connecting")}async _fetchSubscriptionInfo(){this._subscription=await(0,s.De)(this.hass),this._subscription.provider&&this.cloudStatus&&"connected"!==this.cloudStatus.cloud&&this.fire("ha-refresh-cloud-status")}handleLogout(){this.hass.callApi("post","cloud/logout").then((()=>this.fire("ha-refresh-cloud-status")))}_formatSubscription(e){if(null===e)return this.hass.localize("ui.panel.config.cloud.account.fetching_subscription");let t=e.human_description;return e.plan_renewal_date&&(t=t.replace("{periodEnd}",(0,o.o0)(new Date(1e3*e.plan_renewal_date),this.hass.locale))),t}_computeRTLDirection(e){return(0,n.Zu)(e)}}customElements.define("cloud-account",d)}))},14788:(e,t,r)=>{r(53918);var i=r(7599),o=r(5701),n=r(17717),s=r(47181),a=(r(22098),r(43709),r(27434)),l=r(83270);function c(){c=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:r;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!p(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return y(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?y(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=m(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:h(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=h(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function d(e){var t,r=m(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function u(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function p(e){return e.decorators&&e.decorators.length}function f(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function h(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function m(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function y(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}let v=function(e,t,r,i){var o=c();if(i)for(var n=0;n<i.length;n++)o=i[n](o);var s=t((function(e){o.initializeInstanceElements(e,a.elements)}),r),a=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var o,n=e[i];if("method"===n.kind&&(o=t.find(r)))if(f(n.descriptor)||f(o.descriptor)){if(p(n)||p(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(p(n)){if(p(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}u(n,o)}else t.push(n)}return t}(s.d.map(d)),e);return o.initializeClassElements(s.F,a.elements),o.runClassFinishers(s.F,a.finishers)}(null,(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.C)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.C)()],key:"cloudStatus",value:void 0},{kind:"field",decorators:[(0,n.S)()],key:"_syncing",value:()=>!1},{kind:"method",key:"render",value:function(){if(!this.cloudStatus)return i.dy``;const{alexa_enabled:e,alexa_report_state:t}=this.cloudStatus.prefs;return i.dy`
      <ha-card
        header=${this.hass.localize("ui.panel.config.cloud.account.alexa.title")}
      >
        <div class="switch">
          <ha-switch
            .checked=${e}
            @change=${this._enabledToggleChanged}
          ></ha-switch>
        </div>
        <div class="card-content">
          ${this.hass.localize("ui.panel.config.cloud.account.alexa.info")}
          <ul>
            <li>
              <a
                href="https://skills-store.amazon.com/deeplink/dp/B0772J1QKB?deviceType=app"
                target="_blank"
                rel="noreferrer"
              >
                ${this.hass.localize("ui.panel.config.cloud.account.alexa.enable_ha_skill")}
              </a>
            </li>
            <li>
              <a
                href="https://www.nabucasa.com/config/amazon_alexa/"
                target="_blank"
                rel="noreferrer"
              >
                ${this.hass.localize("ui.panel.config.cloud.account.alexa.config_documentation")}
              </a>
            </li>
          </ul>
          ${e?i.dy`
                <div class="state-reporting">
                  <h3>
                    ${this.hass.localize("ui.panel.config.cloud.account.alexa.enable_state_reporting")}
                  </h3>
                  <div class="state-reporting-switch">
                    <ha-switch
                      .checked=${t}
                      @change=${this._reportToggleChanged}
                    ></ha-switch>
                  </div>
                </div>
                <p>
                  ${this.hass.localize("ui.panel.config.cloud.account.alexa.info_state_reporting")}
                </p>
              `:""}
        </div>
        <div class="card-actions">
          <mwc-button
            @click=${this._handleSync}
            .disabled=${!e||this._syncing}
          >
            ${this.hass.localize("ui.panel.config.cloud.account.alexa.sync_entities")}
          </mwc-button>
          <div class="spacer"></div>
          <a href="/config/cloud/alexa">
            <mwc-button
              >${this.hass.localize("ui.panel.config.cloud.account.alexa.manage_entities")}</mwc-button
            >
          </a>
        </div>
      </ha-card>
    `}},{kind:"method",key:"_handleSync",value:async function(){this._syncing=!0;try{await(0,a.z)(this.hass)}catch(e){alert(`${this.hass.localize("ui.panel.config.cloud.account.alexa.sync_entities_error")} ${e.body.message}`)}finally{this._syncing=!1}}},{kind:"method",key:"_enabledToggleChanged",value:async function(e){const t=e.target;try{await(0,l.LV)(this.hass,{alexa_enabled:t.checked}),(0,s.B)(this,"ha-refresh-cloud-status")}catch(e){t.checked=!t.checked}}},{kind:"method",key:"_reportToggleChanged",value:async function(e){const t=e.target;try{await(0,l.LV)(this.hass,{alexa_report_state:t.checked}),(0,s.B)(this,"ha-refresh-cloud-status")}catch(e){alert(`${this.hass.localize("ui.panel.config.cloud.account.alexa.state_reporting_error","enable_disable",this.hass.localize(t.checked?"ui.panel.config.cloud.account.alexa.enable":"ui.panel.config.cloud.account.alexa.disable"))} ${e.message}`),t.checked=!t.checked}}},{kind:"get",static:!0,key:"styles",value:function(){return i.iv`
      a {
        color: var(--primary-color);
      }
      .switch {
        position: absolute;
        right: 24px;
        top: 24px;
      }
      :host([dir="rtl"]) .switch {
        right: auto;
        left: 24px;
      }
      .card-actions {
        display: flex;
      }
      .card-actions a {
        text-decoration: none;
      }
      .spacer {
        flex-grow: 1;
      }
      .state-reporting {
        display: flex;
        margin-top: 1.5em;
      }
      .state-reporting + p {
        margin-top: 0.5em;
      }
      .state-reporting h3 {
        flex-grow: 1;
        margin: 0;
      }
      .state-reporting-switch {
        margin-top: 0.25em;
        margin-right: 7px;
        margin-left: 0.5em;
      }
    `}}]}}),i.oi);customElements.define("cloud-alexa-pref",v)},56969:(e,t,r)=>{r(53918),r(30879);var i=r(7599),o=r(5701),n=r(47181),s=(r(94132),r(22098),r(9381),r(83270)),a=r(26765),l=r(98573);function c(){c=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:r;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!p(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return y(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?y(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=m(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:h(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=h(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function d(e){var t,r=m(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function u(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function p(e){return e.decorators&&e.decorators.length}function f(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function h(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function m(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function y(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}let v=function(e,t,r,i){var o=c();if(i)for(var n=0;n<i.length;n++)o=i[n](o);var s=t((function(e){o.initializeInstanceElements(e,a.elements)}),r),a=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var o,n=e[i];if("method"===n.kind&&(o=t.find(r)))if(f(n.descriptor)||f(o.descriptor)){if(p(n)||p(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(p(n)){if(p(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}u(n,o)}else t.push(n)}return t}(s.d.map(d)),e);return o.initializeClassElements(s.F,a.elements),o.runClassFinishers(s.F,a.finishers)}(null,(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.C)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.C)()],key:"cloudStatus",value:void 0},{kind:"method",key:"render",value:function(){if(!this.cloudStatus)return i.dy``;const{google_enabled:e,google_report_state:t,google_secure_devices_pin:r}=this.cloudStatus.prefs;return i.dy`
      <ha-card
        header=${this.hass.localize("ui.panel.config.cloud.account.google.title")}
      >
        <div class="switch">
          <ha-switch
            id="google_enabled"
            .checked=${e}
            @change=${this._enableToggleChanged}
          ></ha-switch>
        </div>
        <div class="card-content">
          <p>
            ${this.hass.localize("ui.panel.config.cloud.account.google.info")}
          </p>
          ${e&&!this.cloudStatus.google_registered?i.dy`
                <ha-alert
                  .title=${this.hass.localize("ui.panel.config.cloud.account.google.not_configured_title")}
                >
                  ${this.hass.localize("ui.panel.config.cloud.account.google.not_configured_text")}

                  <ul>
                    <li>
                      <a
                        href="https://assistant.google.com/services/a/uid/00000091fd5fb875?hl=en-US"
                        target="_blank"
                        rel="noreferrer"
                      >
                        ${this.hass.localize("ui.panel.config.cloud.account.google.enable_ha_skill")}
                      </a>
                    </li>
                    <li>
                      <a
                        href="https://www.nabucasa.com/config/google_assistant/"
                        target="_blank"
                        rel="noreferrer"
                      >
                        ${this.hass.localize("ui.panel.config.cloud.account.google.config_documentation")}
                      </a>
                    </li>
                  </ul>
                </ha-alert>
              `:""}
          ${e?i.dy`
                <div class="state-reporting">
                  <h3>
                    ${this.hass.localize("ui.panel.config.cloud.account.google.enable_state_reporting")}
                  </h3>
                  <div class="state-reporting-switch">
                    <ha-switch
                      .checked=${t}
                      @change=${this._reportToggleChanged}
                    ></ha-switch>
                  </div>
                </div>
                <p>
                  ${this.hass.localize("ui.panel.config.cloud.account.google.info_state_reporting")}
                </p>
                <div class="secure_devices">
                  <h3>
                    ${this.hass.localize("ui.panel.config.cloud.account.google.security_devices")}
                  </h3>
                  ${this.hass.localize("ui.panel.config.cloud.account.google.enter_pin_info")}
                  <paper-input
                    label=${this.hass.localize("ui.panel.config.cloud.account.google.devices_pin")}
                    id="google_secure_devices_pin"
                    placeholder=${this.hass.localize("ui.panel.config.cloud.account.google.enter_pin_hint")}
                    .value=${r||""}
                    @change=${this._pinChanged}
                  ></paper-input>
                </div>
              `:""}
        </div>
        <div class="card-actions">
          <ha-call-api-button
            .hass=${this.hass}
            .disabled=${!e}
            @hass-api-called=${this._syncEntitiesCalled}
            path="cloud/google_actions/sync"
          >
            ${this.hass.localize("ui.panel.config.cloud.account.google.sync_entities")}
          </ha-call-api-button>
          <a href="/config/cloud/google-assistant">
            <mwc-button>
              ${this.hass.localize("ui.panel.config.cloud.account.google.manage_entities")}
            </mwc-button>
          </a>
        </div>
      </ha-card>
    `}},{kind:"method",key:"_syncEntitiesCalled",value:async function(e){e.detail.success||404!==e.detail.response.status_code||this._syncFailed()}},{kind:"method",key:"_syncFailed",value:async function(){(0,a.Ys)(this,{title:this.hass.localize("ui.panel.config.cloud.account.google.not_configured_title"),text:this.hass.localize("ui.panel.config.cloud.account.google.not_configured_text")}),(0,n.B)(this,"ha-refresh-cloud-status")}},{kind:"method",key:"_enableToggleChanged",value:async function(e){const t=e.target;try{await(0,s.LV)(this.hass,{[t.id]:t.checked}),(0,n.B)(this,"ha-refresh-cloud-status")}catch(e){t.checked=!t.checked}}},{kind:"method",key:"_reportToggleChanged",value:async function(e){const t=e.target;try{await(0,s.LV)(this.hass,{google_report_state:t.checked}),(0,n.B)(this,"ha-refresh-cloud-status")}catch(e){alert(`Unable to ${t.checked?"enable":"disable"} report state. ${e.message}`),t.checked=!t.checked}}},{kind:"method",key:"_pinChanged",value:async function(e){const t=e.target;try{await(0,s.LV)(this.hass,{[t.id]:t.value||null}),(0,l.f)(this,this.hass),(0,n.B)(this,"ha-refresh-cloud-status")}catch(e){alert(`${this.hass.localize("ui.panel.config.cloud.account.google.enter_pin_error")} ${e.message}`),t.value=this.cloudStatus.prefs.google_secure_devices_pin}}},{kind:"get",static:!0,key:"styles",value:function(){return i.iv`
      a {
        color: var(--primary-color);
      }
      .switch {
        position: absolute;
        right: 24px;
        top: 24px;
      }
      :host([dir="rtl"]) .switch {
        right: auto;
        left: 24px;
      }
      ha-call-api-button {
        color: var(--primary-color);
        font-weight: 500;
      }
      paper-input {
        width: 250px;
      }
      .card-actions {
        display: flex;
        justify-content: space-between;
      }
      .card-actions a {
        text-decoration: none;
      }
      .warning {
        color: var(--error-color);
      }
      .secure_devices {
        padding-top: 8px;
      }
      .state-reporting {
        display: flex;
        margin-top: 1.5em;
      }
      .state-reporting + p {
        margin-top: 0.5em;
      }
      h3 {
        margin: 0 0 8px 0;
      }
      .state-reporting h3 {
        flex-grow: 1;
        margin: 0;
      }
      .state-reporting-switch {
        margin-top: 0.25em;
        margin-right: 7px;
        margin-left: 0.5em;
      }
    `}}]}}),i.oi);customElements.define("cloud-google-pref",v)},96112:(e,t,r)=>{r(53918),r(89194);var i=r(7599),o=r(26767),n=r(5701),s=r(47181),a=(r(22098),r(9381),r(43709),r(83270));function l(){l=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:r;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!u(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return m(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?m(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=h(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:f(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=f(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function c(e){var t,r=h(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function d(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function u(e){return e.decorators&&e.decorators.length}function p(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function f(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function h(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function m(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}!function(e,t,r,i){var o=l();if(i)for(var n=0;n<i.length;n++)o=i[n](o);var s=t((function(e){o.initializeInstanceElements(e,a.elements)}),r),a=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var o,n=e[i];if("method"===n.kind&&(o=t.find(r)))if(p(n.descriptor)||p(o.descriptor)){if(u(n)||u(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(u(n)){if(u(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}d(n,o)}else t.push(n)}return t}(s.d.map(c)),e);o.initializeClassElements(s.F,a.elements),o.runClassFinishers(s.F,a.finishers)}([(0,o.M)("cloud-remote-pref")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.C)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.C)()],key:"cloudStatus",value:void 0},{kind:"method",key:"render",value:function(){if(!this.cloudStatus)return i.dy``;const{remote_enabled:e}=this.cloudStatus.prefs,{remote_connected:t,remote_domain:r,remote_certificate:o}=this.cloudStatus;return o?i.dy`
      <ha-card
        header=${this.hass.localize("ui.panel.config.cloud.account.remote.title")}
      >
        <div class="switch">
          <ha-switch
            .checked=${e}
            @change=${this._toggleChanged}
          ></ha-switch>
        </div>
        <div class="card-content">
          ${!t&&e?i.dy`
                <ha-alert
                  .title=${this.hass.localize("ui.panel.config.cloud.account.remote.reconnecting")}
                ></ha-alert>
              `:""}
          ${this.hass.localize("ui.panel.config.cloud.account.remote.info")}
          ${this.hass.localize("ui.panel.config.cloud.account.remote."+(t?"instance_is_available":"instance_will_be_available"))}
          <a
            href="https://${r}"
            target="_blank"
            class="break-word"
            rel="noreferrer"
          >
            https://${r}</a
          >.
        </div>
        <div class="card-actions">
          <a
            href="https://www.nabucasa.com/config/remote/"
            target="_blank"
            rel="noreferrer"
          >
            <mwc-button
              >${this.hass.localize("ui.panel.config.cloud.account.remote.link_learn_how_it_works")}</mwc-button
            >
          </a>
          <div class="spacer"></div>
          <mwc-button @click=${this._openCertInfo}>
            ${this.hass.localize("ui.panel.config.cloud.account.remote.certificate_info")}
          </mwc-button>
        </div>
      </ha-card>
    `:i.dy`
        <ha-card
          header=${this.hass.localize("ui.panel.config.cloud.account.remote.title")}
        >
          <div class="preparing">
            ${this.hass.localize("ui.panel.config.cloud.account.remote.access_is_being_prepared")}
          </div>
        </ha-card>
      `}},{kind:"method",key:"_openCertInfo",value:function(){var e,t;e=this,t={certificateInfo:this.cloudStatus.remote_certificate},(0,s.B)(e,"show-dialog",{dialogTag:"dialog-cloud-certificate",dialogImport:()=>r.e(89394).then(r.bind(r,89394)),dialogParams:t})}},{kind:"method",key:"_toggleChanged",value:async function(e){const t=e.target;try{t.checked?await(0,a.dn)(this.hass):await(0,a.H9)(this.hass),(0,s.B)(this,"ha-refresh-cloud-status")}catch(e){alert(e.message),t.checked=!t.checked}}},{kind:"get",static:!0,key:"styles",value:function(){return i.iv`
      .preparing {
        padding: 0 16px 16px;
      }
      a {
        color: var(--primary-color);
      }
      .switch {
        position: absolute;
        right: 24px;
        top: 24px;
      }
      :host([dir="rtl"]) .switch {
        right: auto;
        left: 24px;
      }
      .warning {
        font-weight: bold;
        margin-bottom: 1em;
      }
      .warning ha-svg-icon {
        color: var(--warning-color);
      }
      .break-word {
        overflow-wrap: break-word;
      }
      .connection-status {
        position: absolute;
        right: 24px;
        top: 24px;
      }
      :host([dir="rtl"]) .switch {
        right: auto;
        left: 24px;
      }
      .card-actions {
        display: flex;
      }
      .card-actions a {
        text-decoration: none;
      }
      .spacer {
        flex-grow: 1;
      }
    `}}]}}),i.oi)},84095:(e,t,r)=>{r(53918),r(46002),r(53973),r(51095);var i=r(7599),o=r(26767),n=r(5701),s=r(17717),a=r(14516),l=r(47181),c=r(85415),d=(r(22098),r(52039),r(43709),r(83270)),u=r(26765),p=r(50921);const f=()=>Promise.all([r.e(29907),r.e(69526),r.e(12844),r.e(86184)]).then(r.bind(r,86184));function h(){h=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:r;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!v(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return b(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?b(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=k(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:w(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=w(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function m(e){var t,r=k(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function y(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function v(e){return e.decorators&&e.decorators.length}function g(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function w(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function k(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function b(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function E(e,t,r){return E="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=_(e)););return e}(e,t);if(i){var o=Object.getOwnPropertyDescriptor(i,t);return o.get?o.get.call(r):o.value}},E(e,t,r||e)}function _(e){return _=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},_(e)}!function(e,t,r,i){var o=h();if(i)for(var n=0;n<i.length;n++)o=i[n](o);var s=t((function(e){o.initializeInstanceElements(e,a.elements)}),r),a=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var o,n=e[i];if("method"===n.kind&&(o=t.find(r)))if(g(n.descriptor)||g(o.descriptor)){if(v(n)||v(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(v(n)){if(v(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}y(n,o)}else t.push(n)}return t}(s.d.map(m)),e);o.initializeClassElements(s.F,a.elements),o.runClassFinishers(s.F,a.finishers)}([(0,o.M)("cloud-tts-pref")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[(0,n.C)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.C)()],key:"cloudStatus",value:void 0},{kind:"field",decorators:[(0,s.S)()],key:"savingPreferences",value:()=>!1},{kind:"field",decorators:[(0,s.S)()],key:"ttsInfo",value:void 0},{kind:"method",key:"render",value:function(){if(!this.cloudStatus)return i.dy``;const e=this.getLanguages(this.ttsInfo),t=this.cloudStatus.prefs.tts_default_voice,r=this.getSupportedGenders(t[0],this.ttsInfo);return i.dy`
      <ha-card
        header=${this.hass.localize("ui.panel.config.cloud.account.tts.title")}
      >
        <div class="card-content">
          ${this.hass.localize("ui.panel.config.cloud.account.tts.info","service",'"tts.cloud_say"')}
          <br /><br />

          <paper-dropdown-menu-light
            .label=${this.hass.localize("ui.panel.config.cloud.account.tts.default_language")}
            .disabled=${this.savingPreferences}
          >
            <paper-listbox
              slot="dropdown-content"
              .selected=${t[0]}
              attr-for-selected="value"
              @iron-select=${this._handleLanguageChange}
            >
              ${e.map((([e,t])=>i.dy`<paper-item .value=${e}>${t}</paper-item>`))}
            </paper-listbox>
          </paper-dropdown-menu-light>

          <paper-dropdown-menu-light .disabled=${this.savingPreferences}>
            <paper-listbox
              slot="dropdown-content"
              .selected=${t[1]}
              attr-for-selected="value"
              @iron-select=${this._handleGenderChange}
            >
              ${r.map((([e,t])=>i.dy`<paper-item .value=${e}>${t}</paper-item>`))}
            </paper-listbox>
          </paper-dropdown-menu-light>
        </div>
        <div class="card-actions">
          <mwc-button @click=${this._openTryDialog}>
            ${this.hass.localize("ui.panel.config.cloud.account.tts.try")}
          </mwc-button>
        </div>
      </ha-card>
    `}},{kind:"method",key:"firstUpdated",value:function(e){E(_(r.prototype),"firstUpdated",this).call(this,e),(0,d.n8)(this.hass).then((e=>{this.ttsInfo=e}))}},{kind:"method",key:"updated",value:function(e){E(_(r.prototype),"updated",this).call(this,e),e.has("cloudStatus")&&(this.savingPreferences=!1)}},{kind:"field",key:"getLanguages",value:()=>(0,a.Z)((e=>{const t=[];if(!e)return t;const r=new Set;for(const[i]of e.languages){if(r.has(i))continue;r.add(i);let e=i;if(i in p.o.translations)e=p.o.translations[i].nativeName;else{const[t,r]=i.split("-");t in p.o.translations&&(e=`${p.o.translations[t].nativeName}`,t.toLowerCase()!==r.toLowerCase()&&(e+=` (${r})`))}t.push([i,e])}return t.sort(((e,t)=>(0,c.f)(e[1],t[1])))}))},{kind:"field",key:"getSupportedGenders",value(){return(0,a.Z)(((e,t)=>{const r=[];if(!t)return r;for(const[i,o]of t.languages)i===e&&r.push([o,this.hass.localize(`ui.panel.config.cloud.account.tts.${o}`)||o]);return r.sort(((e,t)=>(0,c.f)(e[1],t[1])))}))}},{kind:"method",key:"_openTryDialog",value:function(){var e,t;e=this,t={defaultVoice:this.cloudStatus.prefs.tts_default_voice},(0,l.B)(e,"show-dialog",{dialogTag:"dialog-cloud-try-tts",dialogImport:f,dialogParams:t})}},{kind:"method",key:"_handleLanguageChange",value:async function(e){if(e.detail.item.value===this.cloudStatus.prefs.tts_default_voice[0])return;this.savingPreferences=!0;const t=e.detail.item.value,r=this.cloudStatus.prefs.tts_default_voice[1],i=this.getSupportedGenders(t,this.ttsInfo),o=i.find((e=>e[0]===r))?r:i[0][0];try{await(0,d.LV)(this.hass,{tts_default_voice:[t,o]}),(0,l.B)(this,"ha-refresh-cloud-status")}catch(e){this.savingPreferences=!1,console.error(e),(0,u.Ys)(this,{text:`Unable to save default language. ${e}`,warning:!0})}}},{kind:"method",key:"_handleGenderChange",value:async function(e){if(e.detail.item.value===this.cloudStatus.prefs.tts_default_voice[1])return;this.savingPreferences=!0;const t=this.cloudStatus.prefs.tts_default_voice[0],r=e.detail.item.value;try{await(0,d.LV)(this.hass,{tts_default_voice:[t,r]}),(0,l.B)(this,"ha-refresh-cloud-status")}catch(e){this.savingPreferences=!1,console.error(e),(0,u.Ys)(this,{text:`Unable to save default gender. ${e}`,warning:!0})}}},{kind:"get",static:!0,key:"styles",value:function(){return i.iv`
      a {
        color: var(--primary-color);
      }
      .example {
        position: absolute;
        right: 16px;
        top: 16px;
      }
      :host([dir="rtl"]) .example {
        right: auto;
        left: 24px;
      }
    `}}]}}),i.oi)},6163:(e,t,r)=>{r(53973),r(89194);var i=r(7599),o=r(26767),n=r(5701),s=r(17717),a=r(7323),l=(r(22098),r(31206),r(14089),r(43709),r(83270)),c=r(43408),d=r(11654),u=r(47181);function p(){p=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:r;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!m(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return w(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?w(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=g(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:v(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=v(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function f(e){var t,r=g(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function h(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function m(e){return e.decorators&&e.decorators.length}function y(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function v(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function g(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function w(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function k(e,t,r){return k="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=b(e)););return e}(e,t);if(i){var o=Object.getOwnPropertyDescriptor(i,t);return o.get?o.get.call(r):o.value}},k(e,t,r||e)}function b(e){return b=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},b(e)}!function(e,t,r,i){var o=p();if(i)for(var n=0;n<i.length;n++)o=i[n](o);var s=t((function(e){o.initializeInstanceElements(e,a.elements)}),r),a=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var o,n=e[i];if("method"===n.kind&&(o=t.find(r)))if(y(n.descriptor)||y(o.descriptor)){if(m(n)||m(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(m(n)){if(m(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}h(n,o)}else t.push(n)}return t}(s.d.map(f)),e);o.initializeClassElements(s.F,a.elements),o.runClassFinishers(s.F,a.finishers)}([(0,o.M)("cloud-webhooks")],(function(e,t){class o extends t{constructor(...t){super(...t),e(this)}}return{F:o,d:[{kind:"field",decorators:[(0,n.C)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.C)({attribute:!1})],key:"cloudStatus",value:void 0},{kind:"field",decorators:[(0,n.C)({type:Boolean})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,s.S)()],key:"_cloudHooks",value:void 0},{kind:"field",decorators:[(0,s.S)()],key:"_localHooks",value:void 0},{kind:"field",decorators:[(0,s.S)()],key:"_progress",value:()=>[]},{kind:"method",key:"connectedCallback",value:function(){k(b(o.prototype),"connectedCallback",this).call(this),this._fetchData()}},{kind:"method",key:"render",value:function(){return i.dy`
      <ha-card
        header=${this.hass.localize("ui.panel.config.cloud.account.webhooks.title")}
      >
        <div class="card-content">
          ${this.hass.localize("ui.panel.config.cloud.account.webhooks.info")}
          ${this.cloudStatus&&this._localHooks&&this._cloudHooks&&this.hass?0===this._localHooks.length?i.dy`
                <div class="body-text">
                  ${this.hass.localize("ui.panel.config.cloud.account.webhooks.no_hooks_yet")}
                  <a href="/config/integrations"
                    >${this.hass.localize("ui.panel.config.cloud.account.webhooks.no_hooks_yet_link_integration")}
                  </a>
                  ${this.hass.localize("ui.panel.config.cloud.account.webhooks.no_hooks_yet2")}
                  <a href="/config/automation/new"
                    >${this.hass.localize("ui.panel.config.cloud.account.webhooks.no_hooks_yet_link_automation")}</a
                  >.
                </div>
              `:this._localHooks.map((e=>i.dy`
                  <ha-settings-row .narrow=${this.narrow} .entry=${e}>
                    <span slot="heading">
                      ${e.name}
                      ${e.domain!==e.name.toLowerCase()?` (${e.domain})`:""}
                    </span>
                    <span slot="description">${e.webhook_id}</span>
                    ${this._progress.includes(e.webhook_id)?i.dy`
                          <div class="progress">
                            <ha-circular-progress active></ha-circular-progress>
                          </div>
                        `:this._cloudHooks[e.webhook_id]?i.dy`
                          <mwc-button @click=${this._handleManageButton}>
                            ${this.hass.localize("ui.panel.config.cloud.account.webhooks.manage")}
                          </mwc-button>
                        `:i.dy`<ha-switch @click=${this._enableWebhook}>
                        </ha-switch>`}
                  </ha-settings-row>
                `)):i.dy`
                <div class="body-text">
                  ${this.hass.localize("ui.panel.config.cloud.account.webhooks.loading")}
                </div>
              `}
          <div class="footer">
            <a
              href="https://www.nabucasa.com/config/webhooks"
              target="_blank"
              rel="noreferrer"
            >
              ${this.hass.localize("ui.panel.config.cloud.account.webhooks.link_learn_more")}
            </a>
          </div>
        </div>
      </ha-card>
    `}},{kind:"method",key:"updated",value:function(e){k(b(o.prototype),"updated",this).call(this,e),e.has("cloudStatus")&&this.cloudStatus&&(this._cloudHooks=this.cloudStatus.prefs.cloudhooks||{})}},{kind:"method",key:"_showDialog",value:function(e){const t=this._localHooks.find((t=>t.webhook_id===e)),i=this._cloudHooks[e];var o,n;o=this,n={webhook:t,cloudhook:i,disableHook:()=>this._disableWebhook(e)},(0,u.B)(o,"show-dialog",{dialogTag:"dialog-manage-cloudhook",dialogImport:()=>r.e(70975).then(r.bind(r,70975)),dialogParams:n})}},{kind:"method",key:"_handleManageButton",value:function(e){const t=e.currentTarget.parentElement.entry;this._showDialog(t.webhook_id)}},{kind:"method",key:"_enableWebhook",value:async function(e){const t=e.currentTarget.parentElement.entry;let r;this._progress=[...this._progress,t.webhook_id];try{r=await(0,l.AV)(this.hass,t.webhook_id)}catch(e){return void alert(e.message)}finally{this._progress=this._progress.filter((e=>e!==t.webhook_id))}this._cloudHooks={...this._cloudHooks,[t.webhook_id]:r},0===this._progress.length&&this._showDialog(t.webhook_id)}},{kind:"method",key:"_disableWebhook",value:async function(e){this._progress=[...this._progress,e];try{await(0,l.Mc)(this.hass,e)}catch(e){return void alert(`${this.hass.localize("ui.panel.config.cloud.account.webhooks.disable_hook_error_msg")} ${e.message}`)}finally{this._progress=this._progress.filter((t=>t!==e))}const{[e]:t,...r}=this._cloudHooks;this._cloudHooks=r}},{kind:"method",key:"_fetchData",value:async function(){this._localHooks=(0,a.p)(this.hass,"webhook")?await(0,c.H)(this.hass):[]}},{kind:"get",static:!0,key:"styles",value:function(){return[d.Qx,i.iv`
        .body-text {
          padding: 8px 0;
        }
        .webhook {
          display: flex;
          padding: 4px 0;
        }
        .progress {
          margin-right: 16px;
          display: flex;
          flex-direction: column;
          justify-content: center;
        }
        .footer {
          padding-top: 16px;
        }
        .body-text a,
        .footer a {
          color: var(--primary-color);
        }
        ha-settings-row {
          padding: 0;
        }
      `]}}]}}),i.oi)},57673:(e,t,r)=>{r.a(e,(async e=>{r.r(t);var i=r(26767),o=r(5701),n=r(17717),s=r(83849),a=r(18199),l=r(63685),c=(r(40651),e([l]));function d(){d=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:r;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!f(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return v(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?v(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=y(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:m(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=m(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function u(e){var t,r=y(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function p(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function f(e){return e.decorators&&e.decorators.length}function h(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function m(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function y(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function v(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function g(e,t,r){return g="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=w(e)););return e}(e,t);if(i){var o=Object.getOwnPropertyDescriptor(i,t);return o.get?o.get.call(r):o.value}},g(e,t,r||e)}function w(e){return w=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},w(e)}l=(c.then?await c:c)[0];const k=["account","google-assistant","alexa"],b=["login","register","forgot-password"];!function(e,t,r,i){var o=d();if(i)for(var n=0;n<i.length;n++)o=i[n](o);var s=t((function(e){o.initializeInstanceElements(e,a.elements)}),r),a=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var o,n=e[i];if("method"===n.kind&&(o=t.find(r)))if(h(n.descriptor)||h(o.descriptor)){if(f(n)||f(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(f(n)){if(f(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}p(n,o)}else t.push(n)}return t}(s.d.map(u)),e);o.initializeClassElements(s.F,a.elements),o.runClassFinishers(s.F,a.finishers)}([(0,i.M)("ha-config-cloud")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,o.C)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.C)()],key:"isWide",value:void 0},{kind:"field",decorators:[(0,o.C)()],key:"narrow",value:void 0},{kind:"field",decorators:[(0,o.C)()],key:"route",value:void 0},{kind:"field",decorators:[(0,o.C)()],key:"cloudStatus",value:void 0},{kind:"field",key:"routerOptions",value(){return{defaultPage:"login",showLoading:!0,initialLoad:()=>this._cloudStatusLoaded,beforeRender:e=>{if(this.cloudStatus.logged_in){if(!k.includes(e))return"account"}else if(!b.includes(e))return"login"},routes:{login:{tag:"cloud-login"},register:{tag:"cloud-register",load:()=>r.e(93699).then(r.bind(r,93699))},"forgot-password":{tag:"cloud-forgot-password",load:()=>r.e(2958).then(r.bind(r,2958))},account:{tag:"cloud-account"},"google-assistant":{tag:"cloud-google-assistant",load:()=>Promise.all([r.e(62613),r.e(59799),r.e(6294),r.e(74953),r.e(3143),r.e(55983),r.e(27425)]).then(r.bind(r,27425))},alexa:{tag:"cloud-alexa",load:()=>Promise.all([r.e(62613),r.e(59799),r.e(6294),r.e(74953),r.e(3143),r.e(55983),r.e(38654)]).then(r.bind(r,38654))}}}}},{kind:"field",decorators:[(0,n.S)()],key:"_flashMessage",value:()=>""},{kind:"field",decorators:[(0,n.S)()],key:"_loginEmail",value:()=>""},{kind:"field",key:"_resolveCloudStatusLoaded",value:void 0},{kind:"field",key:"_cloudStatusLoaded",value(){return new Promise((e=>{this._resolveCloudStatusLoaded=e}))}},{kind:"method",key:"firstUpdated",value:function(e){g(w(i.prototype),"firstUpdated",this).call(this,e),this.addEventListener("cloud-done",(e=>{this._flashMessage=e.detail.flashMessage,(0,s.c)("/config/cloud/login")}))}},{kind:"method",key:"updated",value:function(e){if(g(w(i.prototype),"updated",this).call(this,e),e.has("cloudStatus")){const t=e.get("cloudStatus");void 0===t?this._resolveCloudStatusLoaded():t.logged_in!==this.cloudStatus.logged_in&&(0,s.c)(this.route.prefix,{replace:!0})}}},{kind:"method",key:"createElement",value:function(e){const t=g(w(i.prototype),"createElement",this).call(this,e);return t.addEventListener("email-changed",(e=>{this._loginEmail=e.detail.value})),t.addEventListener("flash-message-changed",(e=>{this._flashMessage=e.detail.value})),t}},{kind:"method",key:"updatePageEl",value:function(e){this.cloudStatus&&!this.cloudStatus.logged_in&&k.includes(this._currentPage)||("setProperties"in e?e.setProperties({hass:this.hass,email:this._loginEmail,isWide:this.isWide,narrow:this.narrow,cloudStatus:this.cloudStatus,flashMessage:this._flashMessage}):(e.hass=this.hass,e.email=this._loginEmail,e.isWide=this.isWide,e.narrow=this.narrow,e.cloudStatus=this.cloudStatus,e.flashMessage=this._flashMessage))}}]}}),a.n)}))},40651:(e,t,r)=>{r(53918),r(30879),r(53973),r(89194),r(60748);var i=r(50856),o=r(28426),n=r(87744),s=(r(98762),r(22098),r(10983),r(99282),r(60010),r(11052)),a=r(1265),l=r(76389),c=r(83849);const d=(0,l.o)((e=>class extends e{navigate(...e){(0,c.c)(...e)}}));r(3426),r(88165);class u extends((0,a.Z)(d((0,s.I)(o.H3)))){static get template(){return i.d`
      <style include="iron-flex ha-style">
        .content {
          padding-bottom: 24px;
        }
        [slot="introduction"] {
          margin: -1em 0;
        }
        [slot="introduction"] a {
          color: var(--primary-color);
        }
        paper-item {
          cursor: pointer;
        }
        ha-card {
          overflow: hidden;
        }
        ha-card .card-header {
          margin-bottom: -8px;
        }
        h1 {
          @apply --paper-font-headline;
          margin: 0;
        }
        .error {
          color: var(--error-color);
        }
        .card-actions {
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        [hidden] {
          display: none;
        }
        .flash-msg {
          padding-right: 44px;
        }
        .flash-msg ha-icon-button {
          position: absolute;
          top: 4px;
          right: 8px;
          color: var(--secondary-text-color);
        }
        :host([rtl]) .flash-msg ha-icon-button {
          right: auto;
          left: 8px;
        }
        .login-form {
          display: flex;
          flex-direction: column;
        }
        .pwd-forgot-link {
          color: var(--secondary-text-color) !important;
          text-align: right !important;
          align-self: flex-end;
        }
      </style>
      <hass-subpage
        hass="[[hass]]"
        narrow="[[narrow]]"
        header="Home Assistant Cloud"
      >
        <div class="content">
          <ha-config-section is-wide="[[isWide]]">
            <span slot="header">Home Assistant Cloud</span>
            <div slot="introduction">
              <p>[[localize('ui.panel.config.cloud.login.introduction')]]</p>
              <p>
                [[localize('ui.panel.config.cloud.login.introduction2')]]
                <a
                  href="https://www.nabucasa.com"
                  target="_blank"
                  rel="noreferrer"
                >
                  Nabu&nbsp;Casa,&nbsp;Inc</a
                >[[localize('ui.panel.config.cloud.login.introduction2a')]]
              </p>
              <p>[[localize('ui.panel.config.cloud.login.introduction3')]]</p>
              <p>
                <a
                  href="https://www.nabucasa.com"
                  target="_blank"
                  rel="noreferrer"
                >
                  [[localize('ui.panel.config.cloud.login.learn_more_link')]]
                </a>
              </p>
            </div>

            <ha-card hidden$="[[!flashMessage]]">
              <div class="card-content flash-msg">
                [[flashMessage]]
                <ha-icon-button icon="hass:close" on-click="_dismissFlash"
                  >[[localize('ui.panel.config.cloud.login.dismiss')]]</ha-icon-button
                >
                <paper-ripple id="flashRipple" noink=""></paper-ripple>
              </div>
            </ha-card>

            <ha-card
              header="[[localize('ui.panel.config.cloud.login.sign_in')]]"
            >
              <div class="card-content login-form">
                <div class="error" hidden$="[[!_error]]">[[_error]]</div>
                <paper-input
                  label="[[localize('ui.panel.config.cloud.login.email')]]"
                  id="email"
                  type="email"
                  value="{{email}}"
                  on-keydown="_keyDown"
                  error-message="[[localize('ui.panel.config.cloud.login.email_error_msg')]]"
                ></paper-input>
                <paper-input
                  id="password"
                  label="[[localize('ui.panel.config.cloud.login.password')]]"
                  value="{{_password}}"
                  type="password"
                  on-keydown="_keyDown"
                  error-message="[[localize('ui.panel.config.cloud.login.password_error_msg')]]"
                ></paper-input>
                <button
                  class="link pwd-forgot-link"
                  hidden="[[_requestInProgress]]"
                  on-click="_handleForgotPassword"
                >
                  [[localize('ui.panel.config.cloud.login.forgot_password')]]
                </button>
              </div>
              <div class="card-actions">
                <ha-progress-button
                  on-click="_handleLogin"
                  progress="[[_requestInProgress]]"
                  >[[localize('ui.panel.config.cloud.login.sign_in')]]</ha-progress-button
                >
              </div>
            </ha-card>

            <ha-card>
              <paper-item on-click="_handleRegister">
                <paper-item-body two-line="">
                  [[localize('ui.panel.config.cloud.login.start_trial')]]
                  <div secondary="">
                    [[localize('ui.panel.config.cloud.login.trial_info')]]
                  </div>
                </paper-item-body>
                <ha-icon-next></ha-icon-next>
              </paper-item>
            </ha-card>
          </ha-config-section>
        </div>
      </hass-subpage>
    `}static get properties(){return{hass:Object,isWide:Boolean,narrow:Boolean,email:{type:String,notify:!0},_password:{type:String,value:""},_requestInProgress:{type:Boolean,value:!1},flashMessage:{type:String,notify:!0},rtl:{type:Boolean,reflectToAttribute:!0,computed:"_computeRTL(hass)"},_error:String}}static get observers(){return["_inputChanged(email, _password)"]}connectedCallback(){super.connectedCallback(),this.flashMessage&&requestAnimationFrame((()=>requestAnimationFrame((()=>this.$.flashRipple.simulatedRipple()))))}_inputChanged(){this.$.email.invalid=!1,this.$.password.invalid=!1,this._error=!1}_keyDown(e){13===e.keyCode&&(this._handleLogin(),e.preventDefault())}_handleLogin(){let e=!1;this.email&&this.email.includes("@")||(this.$.email.invalid=!0,this.$.email.focus(),e=!0),this._password.length<8&&(this.$.password.invalid=!0,e||(e=!0,this.$.password.focus())),e||(this._requestInProgress=!0,this.hass.callApi("post","cloud/login",{email:this.email,password:this._password}).then((()=>{this.fire("ha-refresh-cloud-status"),this.setProperties({email:"",_password:""})}),(e=>{this._password="";const t=e&&e.body&&e.body.code;if("PasswordChangeRequired"===t)return alert("[[localize('ui.panel.config.cloud.login.alert_password_change_required')]]"),void this.navigate("/config/cloud/forgot-password");const r={_requestInProgress:!1,_error:e&&e.body&&e.body.message?e.body.message:"Unknown error"};"UserNotConfirmed"===t&&(r._error="[[localize('ui.panel.config.cloud.login.alert_email_confirm_necessary')]]"),this.setProperties(r),this.$.email.focus()})))}_handleRegister(){this.flashMessage="",this.navigate("/config/cloud/register")}_handleForgotPassword(){this.flashMessage="",this.navigate("/config/cloud/forgot-password")}_dismissFlash(){setTimeout((()=>{this.flashMessage=""}),200)}_computeRTL(e){return(0,n.HE)(e)}}customElements.define("cloud-login",u)},3426:(e,t,r)=>{r(21384);var i=r(11654);const o=document.createElement("template");o.setAttribute("style","display: none;"),o.innerHTML=`<dom-module id="ha-style">\n  <template>\n    <style>\n    ${i.Qx.cssText}\n    </style>\n  </template>\n</dom-module>`,document.head.appendChild(o.content)},98573:(e,t,r)=>{r.d(t,{f:()=>o});var i=r(81796);const o=(e,t)=>(0,i.C)(e,{message:t.localize("ui.common.successfully_saved")})}}]);
//# sourceMappingURL=dc273a90.js.map