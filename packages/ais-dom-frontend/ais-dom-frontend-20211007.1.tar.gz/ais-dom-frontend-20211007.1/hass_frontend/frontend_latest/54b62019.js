"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[86327],{86327:(t,e,n)=>{n.r(e);var i=n(47181);class s extends HTMLElement{set hass(t){if(!this.content){const t=document.createElement("ha-card");this.content=document.createElement("div"),t.appendChild(this.content),t.style="background: none;",this.appendChild(t),this.addEventListener("click",(function(){this._onClick()}))}const e=this.config.off_image,n=this.config.entity,i=t.states[n],s=i?i.state:"unavailable",c=this.config.class||this.config.entity.replace(".","_");if(this.setAttribute("class",c),i){const t=i.attributes.entity_picture;this.content.innerHTML="playing"===s&&t?`<img src="${t}" width=100% height=100%" style="">`:e?`<img src="${e}" width=100% align="center" style="">`:'<img src="/static/icons/tile-win-310x150.png" width=100% align="center" style="">'}else this.content.innerHTML='<img src="/static/icons/tile-win-310x150.png" width=100% align="center" style="">'}_onClick(){(0,i.B)(this,"hass-more-info",{entityId:this.config.entity})}setConfig(t){if(!t.entity)throw new Error("You need to define an entity");this.config=t}getCardSize(){return 3}}customElements.define("hui-ais-now-playing-poster-card",s)}}]);