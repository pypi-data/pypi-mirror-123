Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const platformicons_1 = require("platformicons");
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const locale_1 = require("app/locale");
const getPlatformName_1 = (0, tslib_1.__importDefault)(require("app/utils/getPlatformName"));
function PlatformList({ platforms = [], direction = 'right', max = 3, size = 16, consistentWidth = false, showCounter = false, className, }) {
    const visiblePlatforms = platforms.slice(0, max);
    const numNotVisiblePlatforms = platforms.length - visiblePlatforms.length;
    const displayCounter = showCounter && !!numNotVisiblePlatforms;
    function renderContent() {
        if (!platforms.length) {
            return <StyledPlatformIcon size={size} platform="default"/>;
        }
        const platformIcons = visiblePlatforms.slice().reverse();
        if (displayCounter) {
            return (<InnerWrapper>
          <PlatformIcons>
            {platformIcons.map((visiblePlatform, index) => (<tooltip_1.default key={visiblePlatform + index} title={(0, getPlatformName_1.default)(visiblePlatform)} containerDisplayMode="inline-flex">
                <StyledPlatformIcon platform={visiblePlatform} size={size}/>
              </tooltip_1.default>))}
          </PlatformIcons>
          <tooltip_1.default title={(0, locale_1.tn)('%s other platform', '%s other platforms', numNotVisiblePlatforms)} containerDisplayMode="inline-flex">
            <Counter>
              {numNotVisiblePlatforms}
              <Plus>{'\u002B'}</Plus>
            </Counter>
          </tooltip_1.default>
        </InnerWrapper>);
        }
        return (<PlatformIcons>
        {platformIcons.map((visiblePlatform, index) => (<StyledPlatformIcon data-test-id={`platform-icon-${visiblePlatform}`} key={visiblePlatform + index} platform={visiblePlatform} size={size}/>))}
      </PlatformIcons>);
    }
    return (<Wrapper consistentWidth={consistentWidth} className={className} size={size} showCounter={displayCounter} direction={direction} max={max}>
      {renderContent()}
    </Wrapper>);
}
exports.default = PlatformList;
function getOverlapWidth(size) {
    return Math.round(size / 4);
}
const commonStyles = ({ theme }) => `
  cursor: default;
  border-radius: ${theme.borderRadius};
  box-shadow: 0 0 0 1px ${theme.background};
  :hover {
    z-index: 1;
  }
`;
const PlatformIcons = (0, styled_1.default)('div') `
  display: flex;
`;
const InnerWrapper = (0, styled_1.default)('div') `
  display: flex;
  position: relative;
`;
const Plus = (0, styled_1.default)('span') `
  font-size: 10px;
`;
const StyledPlatformIcon = (0, styled_1.default)(platformicons_1.PlatformIcon) `
  ${p => commonStyles(p)};
`;
const Counter = (0, styled_1.default)('div') `
  ${p => commonStyles(p)};
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  font-weight: 600;
  font-size: ${p => p.theme.fontSizeExtraSmall};
  background-color: ${p => p.theme.gray200};
  color: ${p => p.theme.gray300};
  padding: 0 1px;
  position: absolute;
  right: -1px;
`;
const Wrapper = (0, styled_1.default)('div') `
  display: flex;
  flex-shrink: 0;
  justify-content: ${p => (p.direction === 'right' ? 'flex-end' : 'flex-start')};
  ${p => p.consistentWidth && `width: ${p.size + (p.max - 1) * getOverlapWidth(p.size)}px;`};

  ${PlatformIcons} {
    ${p => p.showCounter
    ? (0, react_1.css) `
            z-index: 1;
            flex-direction: row-reverse;
            > * :not(:first-child) {
              margin-right: ${p.size * -1 + getOverlapWidth(p.size)}px;
            }
          `
    : (0, react_1.css) `
            > * :not(:first-child) {
              margin-left: ${p.size * -1 + getOverlapWidth(p.size)}px;
            }
          `}
  }

  ${InnerWrapper} {
    padding-right: ${p => p.size / 2 + 1}px;
  }

  ${Counter} {
    height: ${p => p.size}px;
    min-width: ${p => p.size}px;
  }
`;
//# sourceMappingURL=platformList.jsx.map