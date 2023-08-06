Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const eventDataSection_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventDataSection"));
const cspContent_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/cspContent"));
const cspHelp_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/cspHelp"));
const locale_1 = require("app/locale");
function getView(view, data) {
    switch (view) {
        case 'report':
            return <cspContent_1.default data={data}/>;
        case 'raw':
            return <pre>{JSON.stringify({ 'csp-report': data }, null, 2)}</pre>;
        case 'help':
            return <cspHelp_1.default data={data}/>;
        default:
            throw new TypeError(`Invalid view: ${view}`);
    }
}
class CspInterface extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = { view: 'report' };
        this.toggleView = value => {
            this.setState({
                view: value,
            });
        };
    }
    render() {
        const { view } = this.state;
        const { data } = this.props;
        const cleanData = data.original_policy !== 'string'
            ? data
            : Object.assign(Object.assign({}, data), { 
                // Hide the report-uri since this is redundant and silly
                original_policy: data.original_policy.replace(/(;\s+)?report-uri [^;]+/, '') });
        const actions = (<buttonBar_1.default merged active={view}>
        <button_1.default barId="report" size="xsmall" onClick={this.toggleView.bind(this, 'report')}>
          {(0, locale_1.t)('Report')}
        </button_1.default>
        <button_1.default barId="raw" size="xsmall" onClick={this.toggleView.bind(this, 'raw')}>
          {(0, locale_1.t)('Raw')}
        </button_1.default>
        <button_1.default barId="help" size="xsmall" onClick={this.toggleView.bind(this, 'help')}>
          {(0, locale_1.t)('Help')}
        </button_1.default>
      </buttonBar_1.default>);
        const children = getView(view, cleanData);
        return (<eventDataSection_1.default type="csp" title={<h3>{(0, locale_1.t)('CSP Report')}</h3>} actions={actions} wrapTitle={false}>
        {children}
      </eventDataSection_1.default>);
    }
}
exports.default = CspInterface;
//# sourceMappingURL=csp.jsx.map