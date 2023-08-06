import{r as t,_ as o,e,t as s,n as i,a as n,y as a}from"./index-0be8e3ed.js";import"./c.8a8bb18e.js";import{g as c}from"./c.06eb1f48.js";import{a2 as r}from"./c.c606de65.js";const l=(t,o)=>{import("./c.694ac0f2.js");const e=document.createElement("esphome-logs-dialog");e.configuration=t,e.target=o,document.body.append(e)};let p=class extends n{render(){return this._ports?a`
      <mwc-dialog
        open
        heading=${"Show Logs"}
        scrimClickAction
        @closed=${this._handleClose}
      >
        <mwc-list-item
          twoline
          hasMeta
          dialogAction="close"
          .port=${"OTA"}
          @click=${this._pickPort}
        >
          <span>Connect wirelessly</span>
          <span slot="secondary">Requires the device to be online</span>
          ${r}
        </mwc-list-item>

        ${this._ports.map((t=>a`
            <mwc-list-item
              twoline
              hasMeta
              dialogAction="close"
              .port=${t.port}
              @click=${this._pickPort}
            >
              <span>${t.desc}</span>
              <span slot="secondary">${t.port}</span>
              ${r}
            </mwc-list-item>
          `))}

        <mwc-button
          no-attention
          slot="secondaryAction"
          dialogAction="close"
          label="Cancel"
        ></mwc-button>
      </mwc-dialog>
    `:a``}firstUpdated(t){super.firstUpdated(t),c().then((t=>{0===t.length?(this._handleClose(),l(this.configuration,"OTA")):this._ports=t}))}_pickPort(t){l(this.configuration,t.currentTarget.port)}_handleClose(){this.parentNode.removeChild(this)}};p.styles=t`
    mwc-list-item {
      margin: 0 -20px;
    }
  `,o([e()],p.prototype,"configuration",void 0),o([s()],p.prototype,"_ports",void 0),p=o([i("esphome-logs-target-dialog")],p);var d=Object.freeze({__proto__:null});export{d as l,l as o};
