Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const utils_1 = require("app/utils");
const chunk_1 = (0, tslib_1.__importDefault)(require("./chunk"));
function Contexts({ event, group }) {
    const { user, contexts } = event;
    return (<react_1.Fragment>
      {!(0, utils_1.objectIsEmpty)(user) && (<chunk_1.default key="user" type="user" alias="user" group={group} event={event} value={user}/>)}
      {Object.entries(contexts).map(([key, value]) => {
            var _a;
            return (<chunk_1.default key={key} type={(_a = value === null || value === void 0 ? void 0 : value.type) !== null && _a !== void 0 ? _a : ''} alias={key} group={group} event={event} value={value}/>);
        })}
    </react_1.Fragment>);
}
exports.default = Contexts;
//# sourceMappingURL=index.jsx.map