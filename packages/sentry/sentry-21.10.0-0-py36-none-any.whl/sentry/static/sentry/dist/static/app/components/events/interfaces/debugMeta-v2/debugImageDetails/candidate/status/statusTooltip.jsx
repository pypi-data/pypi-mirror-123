Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("../utils");
const _1 = (0, tslib_1.__importDefault)(require("."));
function StatusTooltip({ candidate, hasReprocessWarning }) {
    const { download } = candidate;
    const { label, description, disabled } = (0, utils_1.getStatusTooltipDescription)(candidate, hasReprocessWarning);
    return (<tooltip_1.default title={label && (<Title>
            <Label>{label}</Label>
            {description && <div>{description}</div>}
          </Title>)} disabled={disabled}>
      <_1.default status={download.status}/>
    </tooltip_1.default>);
}
exports.default = StatusTooltip;
const Title = (0, styled_1.default)('div') `
  text-align: left;
`;
const Label = (0, styled_1.default)('div') `
  display: inline-block;
  margin-bottom: ${(0, space_1.default)(0.25)};
`;
//# sourceMappingURL=statusTooltip.jsx.map