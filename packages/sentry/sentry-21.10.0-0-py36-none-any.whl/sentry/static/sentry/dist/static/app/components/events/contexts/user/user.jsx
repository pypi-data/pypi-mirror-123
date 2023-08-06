Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const userAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/userAvatar"));
const errorBoundary_1 = (0, tslib_1.__importDefault)(require("app/components/errorBoundary"));
const contextBlock_1 = (0, tslib_1.__importDefault)(require("app/components/events/contexts/contextBlock"));
const keyValueList_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/keyValueList"));
const utils_1 = require("app/components/events/interfaces/utils");
const metaProxy_1 = require("app/components/events/meta/metaProxy");
const utils_2 = require("app/utils");
const getUnknownData_1 = (0, tslib_1.__importDefault)(require("../getUnknownData"));
const getUserKnownData_1 = (0, tslib_1.__importDefault)(require("./getUserKnownData"));
const types_1 = require("./types");
const userKnownDataValues = [
    types_1.UserKnownDataType.ID,
    types_1.UserKnownDataType.EMAIL,
    types_1.UserKnownDataType.USERNAME,
    types_1.UserKnownDataType.IP_ADDRESS,
    types_1.UserKnownDataType.NAME,
];
const userIgnoredDataValues = [types_1.UserIgnoredDataType.DATA];
function User({ data }) {
    return (<div className="user-widget">
      <div className="pull-left">
        <userAvatar_1.default user={(0, utils_1.removeFilterMaskedEntries)(data)} size={48} gravatar={false}/>
      </div>
      <contextBlock_1.default data={(0, getUserKnownData_1.default)(data, userKnownDataValues)}/>
      <contextBlock_1.default data={(0, getUnknownData_1.default)(data, [...userKnownDataValues, ...userIgnoredDataValues])}/>
      {(0, utils_2.defined)(data === null || data === void 0 ? void 0 : data.data) && (<errorBoundary_1.default mini>
          <keyValueList_1.default data={Object.entries(data.data).map(([key, value]) => ({
                key,
                value,
                subject: key,
                meta: (0, metaProxy_1.getMeta)(data.data, key),
            }))} isContextData/>
        </errorBoundary_1.default>)}
    </div>);
}
exports.default = User;
//# sourceMappingURL=user.jsx.map