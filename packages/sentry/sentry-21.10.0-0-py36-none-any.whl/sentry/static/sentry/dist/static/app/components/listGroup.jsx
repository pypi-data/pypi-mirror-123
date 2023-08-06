Object.defineProperty(exports, "__esModule", { value: true });
exports.ListGroupItem = exports.ListGroup = void 0;
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const ListGroupItem = (0, styled_1.default)('li') `
  position: relative;
  display: block;
  min-height: 36px;
  border: 1px solid ${p => p.theme.border};

  padding: ${(0, space_1.default)(0.5)} ${(0, space_1.default)(1.5)};

  margin-bottom: -1px;
  ${p => (p.centered ? 'text-align: center;' : '')}

  &:first-child {
    border-top-left-radius: ${p => p.theme.borderRadius};
    border-top-right-radius: ${p => p.theme.borderRadius};
  }
  &:last-child {
    border-bottom-left-radius: ${p => p.theme.borderRadius};
    border-bottom-right-radius: ${p => p.theme.borderRadius};
  }
`;
exports.ListGroupItem = ListGroupItem;
const ListGroup = (0, styled_1.default)('ul') `
  box-shadow: 0 1px 0px rgba(0, 0, 0, 0.03);
  background: ${p => p.theme.background};
  padding: 0;
  margin: 0;

  ${p => p.striped
    ? `
    & > li:nth-child(odd) {
      background: ${p.theme.backgroundSecondary};
    }
  `
    : ''}
`;
exports.ListGroup = ListGroup;
//# sourceMappingURL=listGroup.jsx.map