Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const locale_1 = require("app/locale");
const BaseSimilarSpectrum = ({ className }) => (<div className={className}>
    <span>{(0, locale_1.t)('Similar')}</span>
    <SpectrumItem colorIndex={4}/>
    <SpectrumItem colorIndex={3}/>
    <SpectrumItem colorIndex={2}/>
    <SpectrumItem colorIndex={1}/>
    <SpectrumItem colorIndex={0}/>
    <span>{(0, locale_1.t)('Not Similar')}</span>
  </div>);
const SimilarSpectrum = (0, styled_1.default)(BaseSimilarSpectrum) `
  display: flex;
  font-size: ${p => p.theme.fontSizeSmall};
`;
const SpectrumItem = (0, styled_1.default)('span') `
  border-radius: 2px;
  margin: 5px;
  width: 14px;
  ${p => `background-color: ${p.theme.similarity.colors[p.colorIndex]};`};
`;
exports.default = SimilarSpectrum;
//# sourceMappingURL=similarSpectrum.jsx.map