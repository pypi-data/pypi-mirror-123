Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const emptyStateWarning_1 = (0, tslib_1.__importDefault)(require("app/components/emptyStateWarning"));
const panels_1 = require("app/components/panels");
const EmptyState = ({ children }) => (<panels_1.Panel>
    <panels_1.PanelBody>
      <emptyStateWarning_1.default>
        <p>{children}</p>
      </emptyStateWarning_1.default>
    </panels_1.PanelBody>
  </panels_1.Panel>);
exports.default = EmptyState;
//# sourceMappingURL=emptyState.jsx.map