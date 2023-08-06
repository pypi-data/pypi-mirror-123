Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const defaultProps = {
    isLoading: false,
    isReloading: false,
    maskBackgroundColor: theme_1.default.white,
};
function LoadingContainer(props) {
    const { className, children, isReloading, isLoading, maskBackgroundColor } = props;
    const isLoadingOrReloading = isLoading || isReloading;
    return (<Container className={className}>
      {isLoadingOrReloading && (<div>
          <LoadingMask isReloading={isReloading} maskBackgroundColor={maskBackgroundColor}/>
          <Indicator />
        </div>)}
      {children}
    </Container>);
}
exports.default = LoadingContainer;
LoadingContainer.defaultProps = defaultProps;
const Container = (0, styled_1.default)('div') `
  position: relative;
`;
const LoadingMask = (0, styled_1.default)('div') `
  position: absolute;
  z-index: 1;
  background-color: ${p => p.maskBackgroundColor};
  width: 100%;
  height: 100%;
  opacity: ${p => (p.isReloading ? '0.6' : '1')};
`;
const Indicator = (0, styled_1.default)(loadingIndicator_1.default) `
  position: absolute;
  z-index: 3;
  width: 100%;
`;
//# sourceMappingURL=loadingContainer.jsx.map