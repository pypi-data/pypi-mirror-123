"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[91666],{26765:(a,e,s)=>{s.d(e,{Ys:()=>i,g7:()=>c,D9:()=>r});var t=s(47181);const o=()=>Promise.all([s.e(68200),s.e(30879),s.e(29907),s.e(34831),s.e(1281)]).then(s.bind(s,1281)),n=(a,e,s)=>new Promise((n=>{const i=e.cancel,c=e.confirm;(0,t.B)(a,"show-dialog",{dialogTag:"dialog-box",dialogImport:o,dialogParams:{...e,...s,cancel:()=>{n(!(null==s||!s.prompt)&&null),i&&i()},confirm:a=>{n(null==s||!s.prompt||a),c&&c(a)}}})})),i=(a,e)=>n(a,e),c=(a,e)=>n(a,e,{confirmation:!0}),r=(a,e)=>n(a,e,{prompt:!0})},28490:(a,e,s)=>{s.r(e);s(53268),s(12730);var t=s(50856),o=s(28426);s(60010),s(38353),s(63081),s(54909);class n extends o.H3{static get template(){return t.d`
      <style include="iron-flex ha-style">
        .content {
          padding-bottom: 32px;
        }

        .border {
          margin: 32px auto 0;
          border-bottom: 1px solid rgba(0, 0, 0, 0.12);
          max-width: 1040px;
        }
        .narrow .border {
          max-width: 640px;
        }
        .card-actions {
          display: flex;
        }
        .center-container {
          @apply --layout-vertical;
          @apply --layout-center-center;
          height: 70px;
        }
      </style>

      <hass-subpage header="Konfiguracja bramki AIS dom">
        <div class$="[[computeClasses(isWide)]]">
          <ha-config-section is-wide="[[isWide]]">
            <span slot="header">Wyłączenie bramki</span>
            <span slot="introduction"
              >W tej sekcji możesz zrestartować lub całkowicie wyłączyć bramkę
            </span>
            <ha-card header="Restart lub wyłączenie">
              <div class="card-content">
                W tej sekcji możesz zrestartować lub całkowicie wyłączyć bramkę
              </div>
              <div class="card-actions warning">
                <div>
                  <ha-icon-button
                    class="user-button"
                    icon="hass:refresh"
                  ></ha-icon-button>
                  <ha-call-service-button
                    class="warning"
                    hass="[[hass]]"
                    domain="script"
                    service="ais_restart_system"
                    >Uruchom ponownie
                  </ha-call-service-button>
                </div>
                <div>
                  <ha-icon-button
                    class="user-button"
                    icon="hass:stop"
                  ></ha-icon-button>
                  <ha-call-service-button
                    class="warning"
                    hass="[[hass]]"
                    domain="script"
                    service="ais_stop_system"
                    >Wyłącz
                  </ha-call-service-button>
                </div>
              </div>
            </ha-card>
          </ha-config-section>
        </div>
      </hass-subpage>
    `}static get properties(){return{hass:Object,isWide:Boolean,showAdvanced:Boolean}}computeClasses(a){return a?"content":"content narrow"}}customElements.define("ha-config-ais-dom-config-power",n)}}]);
//# sourceMappingURL=ab2c33f0.js.map