Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const contextData_1 = (0, tslib_1.__importDefault)(require("app/components/contextData"));
const eventDataSection_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventDataSection"));
const locale_1 = require("app/locale");
const DeviceInterface = ({ event }) => {
    const data = event.device || {};
    const extras = Object.entries(data.data || {}).map(([key, value]) => {
        return (<tr key={key}>
        <td className="key">{key}</td>
        <td className="value">
          <contextData_1.default data={value}/>
        </td>
      </tr>);
    });
    return (<eventDataSection_1.default type="device" title={(0, locale_1.t)('Device')} wrapTitle>
      <table className="table key-value">
        <tbody>
          {data.name && (<tr>
              <td className="key">Name</td>
              <td className="value">
                <pre>{data.name}</pre>
              </td>
            </tr>)}
          {data.version && (<tr>
              <td className="key">Version</td>
              <td className="value">
                <pre>{data.version}</pre>
              </td>
            </tr>)}
          {data.build && (<tr>
              <td className="key">Build</td>
              <td className="value">
                <pre>{data.build}</pre>
              </td>
            </tr>)}
          {extras}
        </tbody>
      </table>
    </eventDataSection_1.default>);
};
exports.default = DeviceInterface;
//# sourceMappingURL=device.jsx.map