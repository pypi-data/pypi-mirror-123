import{_ as o,e as t,n as i,a as n,y as e,K as s,L as a}from"./index-d602274d.js";import"./c.1acc301b.js";let l=class extends n{render(){return e`
      <esphome-process-dialog
        .heading=${`Clean ${this.configuration}`}
        .type=${"clean"}
        .spawnParams=${{configuration:this.configuration}}
        @closed=${this._handleClose}
      >
        <mwc-button
          slot="secondaryAction"
          dialogAction="close"
          label="Edit"
          @click=${this._openEdit}
        ></mwc-button>
        <mwc-button
          slot="secondaryAction"
          dialogAction="close"
          label="Install"
          @click=${this._openInstall}
        ></mwc-button>
      </esphome-process-dialog>
    `}_openEdit(){s(this.configuration)}_openInstall(){a(this.configuration)}_handleClose(){this.parentNode.removeChild(this)}};o([t()],l.prototype,"configuration",void 0),l=o([i("esphome-clean-dialog")],l);
