Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const chunk_1 = (0, tslib_1.__importDefault)(require("./chunk"));
const Chunks = ({ chunks }) => (<ChunksSpan>
    {chunks.map((chunk, key) => (0, react_1.cloneElement)(<chunk_1.default chunk={chunk}/>, { key }))}
  </ChunksSpan>);
exports.default = Chunks;
const ChunksSpan = (0, styled_1.default)('span') `
  span {
    display: inline;
  }
`;
//# sourceMappingURL=chunks.jsx.map