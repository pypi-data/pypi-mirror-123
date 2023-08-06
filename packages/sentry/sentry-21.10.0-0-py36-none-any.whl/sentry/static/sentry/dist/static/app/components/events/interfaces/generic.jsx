Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const eventDataSection_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventDataSection"));
const keyValueList_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/keyValueList"));
const metaProxy_1 = require("app/components/events/meta/metaProxy");
const locale_1 = require("app/locale");
function getView(view, data) {
    switch (view) {
        case 'report':
            return (<keyValueList_1.default data={Object.entries(data).map(([key, value]) => ({
                    key,
                    value,
                    subject: key,
                    meta: (0, metaProxy_1.getMeta)(data, key),
                }))} isContextData/>);
        case 'raw':
            return <pre>{JSON.stringify({ 'csp-report': data }, null, 2)}</pre>;
        default:
            throw new TypeError(`Invalid view: ${view}`);
    }
}
class GenericInterface extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            view: 'report',
            data: this.props.data,
        };
        this.toggleView = (value) => {
            this.setState({
                view: value,
            });
        };
    }
    render() {
        const { view, data } = this.state;
        const { type } = this.props;
        const title = (<div>
        <buttonBar_1.default merged active={view}>
          <button_1.default barId="report" size="xsmall" onClick={this.toggleView.bind(this, 'report')}>
            {(0, locale_1.t)('Report')}
          </button_1.default>
          <button_1.default barId="raw" size="xsmall" onClick={this.toggleView.bind(this, 'raw')}>
            {(0, locale_1.t)('Raw')}
          </button_1.default>
        </buttonBar_1.default>
        <h3>{(0, locale_1.t)('Report')}</h3>
      </div>);
        const children = getView(view, data);
        return (<eventDataSection_1.default type={type} title={title} wrapTitle={false}>
        {children}
      </eventDataSection_1.default>);
    }
}
exports.default = GenericInterface;
//# sourceMappingURL=generic.jsx.map