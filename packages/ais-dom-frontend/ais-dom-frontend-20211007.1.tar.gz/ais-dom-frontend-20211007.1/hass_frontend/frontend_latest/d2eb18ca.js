"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[17184],{81303:(e,t,r)=>{r(8878);const i=customElements.get("paper-dropdown-menu");customElements.define("ha-paper-dropdown-menu",class extends i{ready(){super.ready(),setTimeout((()=>{"rtl"===window.getComputedStyle(this).direction&&(this.style.textAlign="right")}),100)}})},2939:(e,t,r)=>{r.d(t,{FQ:()=>i,uJ:()=>n,hL:()=>s,OC:()=>o,z3:()=>a,tB:()=>l,Ar:()=>c,L6:()=>d,oB:()=>p});const i=4,n=8,s=16,o=32,a=64,l=128,c=512,d=1024,p=8192},17184:(e,t,r)=>{r.a(e,(async e=>{r.r(t);r(53973),r(51095);var i=r(7599),n=r(26767),s=r(5701),o=r(40095),a=r(31811),l=(r(55905),r(10983),r(81303),r(56007)),c=r(2939),d=e([a]);function p(){p=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var s="static"===n?e:r;this.defineClassElement(s,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!h(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var s=this.decorateConstructor(r,t);return i.push.apply(i,s.finishers),s.finishers=i,s},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,s=n.length-1;s>=0;s--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[s])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),s=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==s.finisher&&r.push(s.finisher),void 0!==s.elements){e=s.elements;for(var o=0;o<e.length-1;o++)for(var a=o+1;a<e.length;a++)if(e[o].key===e[a].key&&e[o].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return b(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?b(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=v(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var s={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),s.initializer=e.initializer),s},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:y(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=y(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function u(e){var t,r=v(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function f(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function h(e){return e.decorators&&e.decorators.length}function m(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function y(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function v(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function b(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}a=(d.then?await d:d)[0];const w=[{translationKey:"start",icon:"hass:play",serviceName:"start",isVisible:e=>(0,o.e)(e,c.oB)},{translationKey:"pause",icon:"hass:pause",serviceName:"pause",isVisible:e=>(0,o.e)(e,c.oB)&&(0,o.e)(e,c.FQ)},{translationKey:"start_pause",icon:"hass:play-pause",serviceName:"start_pause",isVisible:e=>!(0,o.e)(e,c.oB)&&(0,o.e)(e,c.FQ)},{translationKey:"stop",icon:"hass:stop",serviceName:"stop",isVisible:e=>(0,o.e)(e,c.uJ)},{translationKey:"clean_spot",icon:"hass:target-variant",serviceName:"clean_spot",isVisible:e=>(0,o.e)(e,c.L6)},{translationKey:"locate",icon:"hass:map-marker",serviceName:"locate",isVisible:e=>(0,o.e)(e,c.Ar)},{translationKey:"return_home",icon:"hass:home-map-marker",serviceName:"return_to_base",isVisible:e=>(0,o.e)(e,c.hL)}];!function(e,t,r,i){var n=p();if(i)for(var s=0;s<i.length;s++)n=i[s](n);var o=t((function(e){n.initializeInstanceElements(e,a.elements)}),r),a=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===s.key&&e.placement===s.placement},i=0;i<e.length;i++){var n,s=e[i];if("method"===s.kind&&(n=t.find(r)))if(m(s.descriptor)||m(n.descriptor)){if(h(s)||h(n))throw new ReferenceError("Duplicated methods ("+s.key+") can't be decorated.");n.descriptor=s.descriptor}else{if(h(s)){if(h(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+s.key+").");n.decorators=s.decorators}f(s,n)}else t.push(s)}return t}(o.d.map(u)),e);n.initializeClassElements(o.F,a.elements),n.runClassFinishers(o.F,a.finishers)}([(0,n.M)("more-info-vacuum")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,s.C)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.C)()],key:"stateObj",value:void 0},{kind:"method",key:"render",value:function(){if(!this.hass||!this.stateObj)return i.dy``;const e=this.stateObj;return i.dy`
      ${e.state!==l.nZ?i.dy` <div class="flex-horizontal">
            ${(0,o.e)(e,c.tB)?i.dy`
                  <div>
                    <span class="status-subtitle"
                      >${this.hass.localize("ui.dialogs.more_info_control.vacuum.status")}:
                    </span>
                    <span><strong>${e.attributes.status}</strong></span>
                  </div>
                `:""}
            ${(0,o.e)(e,c.z3)&&e.attributes.battery_level?i.dy`
                  <div>
                    <span>
                      ${e.attributes.battery_level} %
                      <ha-icon
                        .icon=${e.attributes.battery_icon}
                      ></ha-icon>
                    </span>
                  </div>
                `:""}
          </div>`:""}
      ${w.some((t=>t.isVisible(e)))?i.dy`
            <div>
              <p></p>
              <div class="status-subtitle">
                ${this.hass.localize("ui.dialogs.more_info_control.vacuum.commands")}
              </div>
              <div class="flex-horizontal">
                ${w.filter((t=>t.isVisible(e))).map((t=>i.dy`
                    <div>
                      <ha-icon-button
                        .icon=${t.icon}
                        .entry=${t}
                        @click=${this.callService}
                        .title=${this.hass.localize(`ui.dialogs.more_info_control.vacuum.${t.translationKey}`)}
                        .disabled=${e.state===l.nZ}
                      ></ha-icon-button>
                    </div>
                  `))}
              </div>
            </div>
          `:""}
      ${(0,o.e)(e,c.OC)?i.dy`
            <div>
              <div class="flex-horizontal">
                <ha-paper-dropdown-menu
                  .label=${this.hass.localize("ui.dialogs.more_info_control.vacuum.fan_speed")}
                  .disabled=${e.state===l.nZ}
                >
                  <paper-listbox
                    slot="dropdown-content"
                    .selected=${e.attributes.fan_speed}
                    @iron-select=${this.handleFanSpeedChanged}
                    attr-for-selected="item-name"
                  >
                    ${e.attributes.fan_speed_list.map((e=>i.dy`
                        <paper-item .itemName=${e}> ${e} </paper-item>
                      `))}
                  </paper-listbox>
                </ha-paper-dropdown-menu>
                <div
                  style="justify-content: center; align-self: center; padding-top: 1.3em"
                >
                  <span>
                    <ha-icon icon="hass:fan"></ha-icon>
                    ${e.attributes.fan_speed}
                  </span>
                </div>
              </div>
              <p></p>
            </div>
          `:""}

      <ha-attributes
        .hass=${this.hass}
        .stateObj=${this.stateObj}
        .extraFilters=${"fan_speed,fan_speed_list,status,battery_level,battery_icon"}
      ></ha-attributes>
    `}},{kind:"method",key:"callService",value:function(e){const t=e.target.entry;this.hass.callService("vacuum",t.serviceName,{entity_id:this.stateObj.entity_id})}},{kind:"method",key:"handleFanSpeedChanged",value:function(e){const t=this.stateObj.attributes.fan_speed,r=e.detail.item.itemName;r&&t!==r&&this.hass.callService("vacuum","set_fan_speed",{entity_id:this.stateObj.entity_id,fan_speed:r})}},{kind:"get",static:!0,key:"styles",value:function(){return i.iv`
      :host {
        line-height: 1.5;
      }
      .status-subtitle {
        color: var(--secondary-text-color);
      }
      paper-item {
        cursor: pointer;
      }
      .flex-horizontal {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
      }
    `}}]}}),i.oi)}))}}]);
//# sourceMappingURL=d2eb18ca.js.map