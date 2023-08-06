Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const ShortId = ({ shortId, avatar }) => (<Wrapper>
    <AvatarWrapper>{avatar}</AvatarWrapper>
    <IdWrapper>{shortId}</IdWrapper>
  </Wrapper>);
exports.default = ShortId;
const Wrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  white-space: nowrap;
  text-overflow: ellipsis;
  font-size: ${p => p.theme.fontSizeExtraSmall};
`;
const AvatarWrapper = (0, styled_1.default)('div') `
  margin-right: 3px;
  flex-shrink: 0;
`;
const IdWrapper = (0, styled_1.default)('div') `
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-top: 1px;
`;
//# sourceMappingURL=shortId.jsx.map