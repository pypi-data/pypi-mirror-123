Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const hovercard_1 = (0, tslib_1.__importDefault)(require("app/components/hovercard"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const SourceSuggestionExamples = ({ examples, sourceName }) => (<Wrapper>
    <ExampleCard position="right" header={(0, locale_1.t)('Examples for %s in current event', <code>{sourceName}</code>)} body={examples.map(example => (<pre key={example}>{example}</pre>))}>
      <Content>
        {(0, locale_1.t)('See Example')} <icons_1.IconQuestion size="xs"/>
      </Content>
    </ExampleCard>
  </Wrapper>);
exports.default = SourceSuggestionExamples;
const ExampleCard = (0, styled_1.default)(hovercard_1.default) `
  width: 400px;

  pre:last-child {
    margin: 0;
  }
`;
const Content = (0, styled_1.default)('span') `
  display: inline-grid;
  grid-template-columns: repeat(2, max-content);
  align-items: center;
  grid-gap: ${(0, space_1.default)(0.5)};
  color: ${p => p.theme.gray400};
  font-size: ${p => p.theme.fontSizeSmall};
  text-decoration: underline;
  text-decoration-style: dotted;
`;
const Wrapper = (0, styled_1.default)('div') `
  grid-column: 3/3;
`;
//# sourceMappingURL=sourceSuggestionExamples.jsx.map