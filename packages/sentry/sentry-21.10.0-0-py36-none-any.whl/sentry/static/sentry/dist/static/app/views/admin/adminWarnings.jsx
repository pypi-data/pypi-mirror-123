Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const locale_1 = require("app/locale");
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
class AdminWarnings extends asyncView_1.default {
    getEndpoints() {
        return [['data', '/internal/warnings/']];
    }
    renderBody() {
        const { data } = this.state;
        if (data === null) {
            return null;
        }
        const { groups, warnings } = data;
        return (<div>
        <h3>{(0, locale_1.t)('System Warnings')}</h3>
        {!warnings && !groups && (0, locale_1.t)('There are no warnings at this time')}

        {groups.map(([groupName, groupedWarnings]) => (<react_1.Fragment key={groupName}>
            <h4>{groupName}</h4>
            <ul>
              {groupedWarnings.map((warning, i) => (<li key={i}>{warning}</li>))}
            </ul>
          </react_1.Fragment>))}

        {warnings.length > 0 && (<react_1.Fragment>
            <h4>Miscellaneous</h4>
            <ul>
              {warnings.map((warning, i) => (<li key={i}>{warning}</li>))}
            </ul>
          </react_1.Fragment>)}
      </div>);
    }
}
exports.default = AdminWarnings;
//# sourceMappingURL=adminWarnings.jsx.map