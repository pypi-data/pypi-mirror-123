Object.defineProperty(exports, "__esModule", { value: true });
exports.AdminRelays = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const linkWithConfirmation_1 = (0, tslib_1.__importDefault)(require("app/components/links/linkWithConfirmation"));
const resultGrid_1 = (0, tslib_1.__importDefault)(require("app/components/resultGrid"));
const locale_1 = require("app/locale");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const prettyDate = (x) => (0, moment_1.default)(x).format('ll LTS');
class AdminRelays extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            loading: false,
        };
    }
    onDelete(key) {
        this.setState({ loading: true });
        this.props.api.request(`/relays/${key}/`, {
            method: 'DELETE',
            success: () => this.setState({ loading: false }),
            error: () => this.setState({ loading: false }),
        });
    }
    getRow(row) {
        return [
            <td key="id">
        <strong>{row.relayId}</strong>
      </td>,
            <td key="key">{row.publicKey}</td>,
            <td key="firstSeen" style={{ textAlign: 'right' }}>
        {prettyDate(row.firstSeen)}
      </td>,
            <td key="lastSeen" style={{ textAlign: 'right' }}>
        {prettyDate(row.lastSeen)}
      </td>,
            <td key="tools" style={{ textAlign: 'right' }}>
        <span className="editor-tools">
          <linkWithConfirmation_1.default className="danger" title="Remove" message={(0, locale_1.t)('Are you sure you wish to delete this relay?')} onConfirm={() => this.onDelete(row.id)}>
            {(0, locale_1.t)('Remove')}
          </linkWithConfirmation_1.default>
        </span>
      </td>,
        ];
    }
    render() {
        const columns = [
            <th key="id" style={{ width: 350, textAlign: 'left' }}>
        Relay
      </th>,
            <th key="key">Public Key</th>,
            <th key="firstSeen" style={{ width: 150, textAlign: 'right' }}>
        First seen
      </th>,
            <th key="lastSeen" style={{ width: 150, textAlign: 'right' }}>
        Last seen
      </th>,
            <th key="tools"/>,
        ];
        return (<div>
        <h3>{(0, locale_1.t)('Relays')}</h3>
        <resultGrid_1.default path="/manage/relays/" endpoint="/relays/" method="GET" columns={columns} columnsForRow={this.getRow} hasSearch={false} sortOptions={[
                ['firstSeen', 'First seen'],
                ['lastSeen', 'Last seen'],
                ['relayId', 'Relay ID'],
            ]} defaultSort="firstSeen" {...this.props}/>
      </div>);
    }
}
exports.AdminRelays = AdminRelays;
exports.default = (0, withApi_1.default)(AdminRelays);
//# sourceMappingURL=adminRelays.jsx.map