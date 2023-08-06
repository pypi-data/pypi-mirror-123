import{r as t,_ as o,e,t as s,n as i,a as n,y as a}from"./index-3596f402.js";import"./c.e7601da3.js";import{g as r}from"./c.02180161.js";import{a2 as c}from"./c.7f9fedec.js";const l=(t,o)=>{import("./c.55128935.js");const e=document.createElement("esphome-logs-dialog");e.configuration=t,e.target=o,document.body.append(e)};let p=class extends n{render(){return this._ports?a`
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
          ${c}
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
              ${c}
            </mwc-list-item>
          `))}

        <mwc-button
          no-attention
          slot="secondaryAction"
          dialogAction="close"
          label="Cancel"
        ></mwc-button>
      </mwc-dialog>
    `:a``}firstUpdated(t){super.firstUpdated(t),r().then((t=>{0===t.length?(this._handleClose(),l(this.configuration,"OTA")):this._ports=t}))}_pickPort(t){l(this.configuration,t.currentTarget.port)}_handleClose(){this.parentNode.removeChild(this)}};p.styles=t`
    mwc-list-item {
      margin: 0 -20px;
    }
  `,o([e()],p.prototype,"configuration",void 0),o([s()],p.prototype,"_ports",void 0),p=o([i("esphome-logs-target-dialog")],p);var d=Object.freeze({__proto__:null});export{d as l,l as o};
