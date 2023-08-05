"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[6169],{6169:(e,t,s)=>{s.a(e,(async e=>{s.r(t);var r=s(7599),i=s(50467),n=s(99476),o=e([n]);n=(o.then?await o:o)[0];const a={1:5,2:3,3:2};class d extends n.p{static async getConfigElement(){return await Promise.all([s.e(75009),s.e(78161),s.e(42955),s.e(88985),s.e(28055),s.e(26561),s.e(62613),s.e(59799),s.e(6294),s.e(69505),s.e(93098),s.e(89841),s.e(77426),s.e(46002),s.e(56087),s.e(22001),s.e(2905),s.e(73401),s.e(81480),s.e(87482),s.e(74535),s.e(68331),s.e(68101),s.e(36902),s.e(60033),s.e(18900),s.e(20515),s.e(66442),s.e(9665),s.e(74513),s.e(22382)]).then(s.bind(s,22382)),document.createElement("hui-grid-card-editor")}async getCardSize(){if(!this._cards||!this._config)return 0;if(this.square){const e=a[this.columns]||1;return(this._cards.length<this.columns?e:this._cards.length/this.columns*e)+(this._config.title?1:0)}const e=[];for(const t of this._cards)e.push((0,i.N)(t));const t=await Promise.all(e);let s=this._config.title?1:0;for(let e=0;e<t.length;e+=this.columns)s+=Math.max(...t.slice(e,e+this.columns));return s}get columns(){var e;return(null===(e=this._config)||void 0===e?void 0:e.columns)||3}get square(){var e;return!1!==(null===(e=this._config)||void 0===e?void 0:e.square)}setConfig(e){super.setConfig(e),this.style.setProperty("--grid-card-column-count",String(this.columns)),this.square?this.setAttribute("square",""):this.removeAttribute("square")}static get styles(){return[super.sharedStyles,r.iv`
        #root {
          display: grid;
          grid-template-columns: repeat(
            var(--grid-card-column-count, ${3}),
            minmax(0, 1fr)
          );
          grid-gap: var(--grid-card-gap, 8px);
        }
        :host([square]) #root {
          grid-auto-rows: 1fr;
        }
        :host([square]) #root::before {
          content: "";
          width: 0;
          padding-bottom: 100%;
          grid-row: 1 / 1;
          grid-column: 1 / 1;
        }

        :host([square]) #root > *:not([hidden]) {
          grid-row: 1 / 1;
          grid-column: 1 / 1;
        }
        :host([square]) #root > *:not([hidden]) ~ *:not([hidden]) {
          /*
	       * Remove grid-row and grid-column from every element that comes after
	       * the first not-hidden element
	       */
          grid-row: unset;
          grid-column: unset;
        }
      `]}}customElements.define("hui-grid-card",d)}))}}]);
//# sourceMappingURL=f7e030eb.js.map