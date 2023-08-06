Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const eventDataSection_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventDataSection"));
const annotated_1 = (0, tslib_1.__importDefault)(require("app/components/events/meta/annotated"));
const locale_1 = require("app/locale");
const EventSdk = ({ sdk }) => (<eventDataSection_1.default type="sdk" title={(0, locale_1.t)('SDK')}>
    <table className="table key-value">
      <tbody>
        <tr key="name">
          <td className="key">{(0, locale_1.t)('Name')}</td>
          <td className="value">
            <annotated_1.default object={sdk} objectKey="name">
              {value => <pre className="val-string">{value}</pre>}
            </annotated_1.default>
          </td>
        </tr>
        <tr key="version">
          <td className="key">{(0, locale_1.t)('Version')}</td>
          <td className="value">
            <annotated_1.default object={sdk} objectKey="version">
              {value => <pre className="val-string">{value}</pre>}
            </annotated_1.default>
          </td>
        </tr>
      </tbody>
    </table>
  </eventDataSection_1.default>);
exports.default = EventSdk;
//# sourceMappingURL=eventSdk.jsx.map