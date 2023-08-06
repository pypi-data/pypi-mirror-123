Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const EmptyState = () => (<panels_1.Panel>
    <emptyMessage_1.default>{(0, locale_1.t)('No Keys Registered.')}</emptyMessage_1.default>
  </panels_1.Panel>);
exports.default = EmptyState;
//# sourceMappingURL=emptyState.jsx.map