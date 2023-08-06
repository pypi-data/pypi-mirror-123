Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const avatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/views/settings/account/notifications/utils");
// TODO(mgaeta): Infer parentKey from parent.
const ParentLabel = ({ notificationType, parent }) => (<FieldLabel>
    <avatar_1.default {...{
    [(0, utils_1.getParentKey)(notificationType)]: parent,
}}/>
    <span>{parent.slug}</span>
  </FieldLabel>);
const FieldLabel = (0, styled_1.default)('div') `
  display: flex;
  gap: ${(0, space_1.default)(0.5)};
  line-height: 16px;
`;
exports.default = ParentLabel;
//# sourceMappingURL=parentLabel.jsx.map