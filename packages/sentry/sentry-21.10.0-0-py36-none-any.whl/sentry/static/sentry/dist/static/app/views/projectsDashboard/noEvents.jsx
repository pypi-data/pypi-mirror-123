Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const locale_1 = require("app/locale");
const NoEvents = ({ seriesCount }) => (<Container>
    <EmptyText seriesCount={seriesCount}>{(0, locale_1.t)('No activity yet.')}</EmptyText>
  </Container>);
exports.default = NoEvents;
const Container = (0, styled_1.default)('div') `
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
`;
const EmptyText = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 4px;
  margin-right: 4px;
  height: ${p => (p.seriesCount > 1 ? '90px' : '150px')};
  color: ${p => p.theme.gray300};
`;
//# sourceMappingURL=noEvents.jsx.map