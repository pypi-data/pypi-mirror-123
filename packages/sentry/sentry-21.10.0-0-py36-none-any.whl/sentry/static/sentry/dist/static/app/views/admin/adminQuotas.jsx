Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const forms_1 = require("app/components/forms");
const internalStatChart_1 = (0, tslib_1.__importDefault)(require("app/components/internalStatChart"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
class AdminQuotas extends asyncView_1.default {
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { since: new Date().getTime() / 1000 - 3600 * 24 * 7, resolution: '1h' });
    }
    getEndpoints() {
        return [['config', '/internal/quotas/']];
    }
    renderBody() {
        const { config } = this.state;
        return (<div>
        <h3>Quotas</h3>

        <div className="box">
          <div className="box-header">
            <h4>Config</h4>
          </div>

          <div className="box-content with-padding">
            <forms_1.TextField name="backend" value={config.backend} label="Backend" disabled/>
            <forms_1.TextField name="rateLimit" value={config.options['system.rate-limit']} label="Rate Limit" disabled/>
          </div>
        </div>

        <div className="box">
          <div className="box-header">
            <h4>Total Events</h4>
          </div>
          <internalStatChart_1.default since={this.state.since} resolution={this.state.resolution} stat="events.total" label="Events"/>
        </div>

        <div className="box">
          <div className="box-header">
            <h4>Dropped Events</h4>
          </div>
          <internalStatChart_1.default since={this.state.since} resolution={this.state.resolution} stat="events.dropped" label="Events"/>
        </div>
      </div>);
    }
}
exports.default = AdminQuotas;
//# sourceMappingURL=adminQuotas.jsx.map