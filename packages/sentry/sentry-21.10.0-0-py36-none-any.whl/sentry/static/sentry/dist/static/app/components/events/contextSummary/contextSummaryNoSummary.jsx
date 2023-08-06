Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const item_1 = (0, tslib_1.__importDefault)(require("./item"));
const ContextSummaryNoSummary = ({ title }) => (<item_1.default icon={<span className="context-item-icon"/>}>
    <h3 data-test-id="no-summary-title">{title}</h3>
  </item_1.default>);
exports.default = ContextSummaryNoSummary;
//# sourceMappingURL=contextSummaryNoSummary.jsx.map