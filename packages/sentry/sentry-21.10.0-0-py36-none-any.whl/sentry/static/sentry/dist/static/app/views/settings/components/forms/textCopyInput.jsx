Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_dom_1 = (0, tslib_1.__importDefault)(require("react-dom"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const clipboard_1 = (0, tslib_1.__importDefault)(require("app/components/clipboard"));
const icons_1 = require("app/icons");
const input_1 = require("app/styles/input");
const selectText_1 = require("app/utils/selectText");
const Wrapper = (0, styled_1.default)('div') `
  display: flex;
`;
const StyledInput = (0, styled_1.default)('input') `
  ${input_1.inputStyles};
  background-color: ${p => p.theme.backgroundSecondary};
  border-right-width: 0;
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
  direction: ${p => (p.rtl ? 'rtl' : 'ltr')};

  &:hover,
  &:focus {
    background-color: ${p => p.theme.backgroundSecondary};
    border-right-width: 0;
  }
`;
const OverflowContainer = (0, styled_1.default)('div') `
  flex-grow: 1;
  border: none;
`;
const StyledCopyButton = (0, styled_1.default)(button_1.default) `
  flex-shrink: 1;
  border-radius: 0 0.25em 0.25em 0;
  box-shadow: none;
`;
class TextCopyInput extends React.Component {
    constructor() {
        super(...arguments);
        this.textRef = React.createRef();
        // Select text when copy button is clicked
        this.handleCopyClick = (e) => {
            if (!this.textRef.current) {
                return;
            }
            const { onCopy, children } = this.props;
            this.handleSelectText();
            onCopy === null || onCopy === void 0 ? void 0 : onCopy(children, e);
            e.stopPropagation();
        };
        this.handleSelectText = () => {
            const { rtl } = this.props;
            if (!this.textRef.current) {
                return;
            }
            // We use findDOMNode here because `this.textRef` is not a dom node,
            // it's a ref to AutoSelectText
            const node = react_dom_1.default.findDOMNode(this.textRef.current); // eslint-disable-line react/no-find-dom-node
            if (!node || !(node instanceof HTMLElement)) {
                return;
            }
            if (rtl && node instanceof HTMLInputElement) {
                // we don't want to select the first character - \u202A, nor the last - \u202C
                node.setSelectionRange(1, node.value.length - 1);
            }
            else {
                (0, selectText_1.selectText)(node);
            }
        };
    }
    render() {
        const { style, children, rtl } = this.props;
        /**
         * We are using direction: rtl; to always show the ending of a long overflowing text in input.
         *
         * This however means that the trailing characters with BiDi class O.N. ('Other Neutrals') goes to the other side.
         * Hello! becomes !Hello and vice versa. This is a problem for us when we want to show path in this component, because
         * /user/local/bin becomes user/local/bin/. Wrapping in unicode characters for left-to-righ embedding solves this,
         * however we need to be aware of them when selecting the text - we are solving that by offseting the selectionRange.
         */
        const inputValue = rtl ? '\u202A' + children + '\u202C' : children;
        return (<Wrapper>
        <OverflowContainer>
          <StyledInput readOnly ref={this.textRef} style={style} value={inputValue} onClick={this.handleSelectText} rtl={rtl}/>
        </OverflowContainer>
        <clipboard_1.default hideUnsupported value={children}>
          <StyledCopyButton type="button" size="xsmall" onClick={this.handleCopyClick}>
            <icons_1.IconCopy />
          </StyledCopyButton>
        </clipboard_1.default>
      </Wrapper>);
    }
}
exports.default = TextCopyInput;
//# sourceMappingURL=textCopyInput.jsx.map