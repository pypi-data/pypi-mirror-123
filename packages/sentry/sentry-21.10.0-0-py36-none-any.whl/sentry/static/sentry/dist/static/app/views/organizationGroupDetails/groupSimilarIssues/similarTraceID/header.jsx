Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const clipboard_1 = (0, tslib_1.__importDefault)(require("app/components/clipboard"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const events_1 = require("app/utils/events");
const Header = ({ traceID }) => (<Wrapper>
    <h4>{(0, locale_1.t)('Issues with the same trace ID')}</h4>
    {traceID ? (<clipboard_1.default value={traceID}>
        <ClipboardWrapper>
          <span>{(0, events_1.getShortEventId)(traceID)}</span>
          <icons_1.IconCopy />
        </ClipboardWrapper>
      </clipboard_1.default>) : (<span>{'-'}</span>)}
  </Wrapper>);
exports.default = Header;
const Wrapper = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: max-content 1fr;
  grid-gap: ${(0, space_1.default)(1)};
  align-items: center;
  font-size: ${p => p.theme.headerFontSize};
  color: ${p => p.theme.gray300};
  h4 {
    font-size: ${p => p.theme.headerFontSize};
    color: ${p => p.theme.textColor};
    font-weight: normal;
    margin-bottom: 0;
  }
`;
const ClipboardWrapper = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: max-content 1fr;
  grid-gap: ${(0, space_1.default)(1)};
  align-items: center;
  &:hover {
    cursor: pointer;
  }
`;
//# sourceMappingURL=header.jsx.map