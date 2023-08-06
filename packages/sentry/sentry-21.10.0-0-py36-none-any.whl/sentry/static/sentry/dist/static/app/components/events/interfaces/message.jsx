Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const eventDataSection_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventDataSection"));
const keyValueList_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/keyValueList"));
const annotated_1 = (0, tslib_1.__importDefault)(require("app/components/events/meta/annotated"));
const metaProxy_1 = require("app/components/events/meta/metaProxy");
const locale_1 = require("app/locale");
const utils_1 = require("app/utils");
const Message = ({ data }) => {
    const renderParams = () => {
        const params = data === null || data === void 0 ? void 0 : data.params;
        if (!params || (0, utils_1.objectIsEmpty)(params)) {
            return null;
        }
        // NB: Always render params, regardless of whether they appear in the
        // formatted string due to structured logging frameworks, like Serilog. They
        // only format some parameters into the formatted string, but we want to
        // display all of them.
        if (Array.isArray(params)) {
            const arrayData = params.map((value, i) => {
                const key = `#${i}`;
                return {
                    key,
                    value,
                    subject: key,
                };
            });
            return <keyValueList_1.default data={arrayData} isSorted={false} isContextData/>;
        }
        const objectData = Object.entries(params).map(([key, value]) => ({
            key,
            value,
            subject: key,
            meta: (0, metaProxy_1.getMeta)(params, key),
        }));
        return <keyValueList_1.default data={objectData} isSorted={false} isContextData/>;
    };
    return (<eventDataSection_1.default type="message" title={(0, locale_1.t)('Message')}>
      <annotated_1.default object={data} objectKey="formatted">
        {value => <pre className="plain">{value}</pre>}
      </annotated_1.default>
      {renderParams()}
    </eventDataSection_1.default>);
};
exports.default = Message;
//# sourceMappingURL=message.jsx.map