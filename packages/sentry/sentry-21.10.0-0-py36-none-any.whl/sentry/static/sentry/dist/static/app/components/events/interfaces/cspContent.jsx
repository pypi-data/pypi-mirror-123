Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const keyValueList_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/keyValueList"));
const metaProxy_1 = require("app/components/events/meta/metaProxy");
function CSPContent({ data }) {
    return (<div>
      <h4>
        <span>{data.effective_directive}</span>
      </h4>
      <keyValueList_1.default data={Object.entries(data).map(([key, value]) => ({
            key,
            subject: key,
            value,
            meta: (0, metaProxy_1.getMeta)(data, key),
        }))} isContextData/>
    </div>);
}
exports.default = CSPContent;
//# sourceMappingURL=cspContent.jsx.map