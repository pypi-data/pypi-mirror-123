Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const rules_1 = (0, tslib_1.__importDefault)(require("./rules"));
const Content = ({ rules, disabled, onDeleteRule, onEditRule }) => {
    if (rules.length === 0) {
        return (<emptyMessage_1.default icon={<icons_1.IconWarning size="xl"/>} description={(0, locale_1.t)('You have no data scrubbing rules')}/>);
    }
    return (<rules_1.default rules={rules} onDeleteRule={onDeleteRule} onEditRule={onEditRule} disabled={disabled}/>);
};
exports.default = Content;
//# sourceMappingURL=content.jsx.map