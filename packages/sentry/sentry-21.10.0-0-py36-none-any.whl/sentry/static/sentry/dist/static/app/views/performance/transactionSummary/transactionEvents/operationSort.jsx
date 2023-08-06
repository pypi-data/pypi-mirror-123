Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_dom_1 = (0, tslib_1.__importDefault)(require("react-dom"));
const react_popper_1 = require("react-popper");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const menuItem_1 = (0, tslib_1.__importDefault)(require("app/components/menuItem"));
const radio_1 = (0, tslib_1.__importDefault)(require("app/components/radio"));
const locale_1 = require("app/locale");
class OperationSort extends react_1.Component {
    constructor(props) {
        super(props);
        this.state = {
            isOpen: false,
        };
        this.handleClickOutside = (event) => {
            if (!this.menuEl) {
                return;
            }
            if (!(event.target instanceof Element)) {
                return;
            }
            if (this.menuEl.contains(event.target)) {
                return;
            }
            this.setState({ isOpen: false });
        };
        this.toggleOpen = () => {
            this.setState(({ isOpen }) => ({ isOpen: !isOpen }));
        };
        let portal = document.getElementById('transaction-events-portal');
        if (!portal) {
            portal = document.createElement('div');
            portal.setAttribute('id', 'transaction-events-portal');
            document.body.appendChild(portal);
        }
        this.portalEl = portal;
        this.menuEl = null;
    }
    componentDidUpdate(_props, prevState) {
        if (this.state.isOpen && prevState.isOpen === false) {
            document.addEventListener('click', this.handleClickOutside, true);
        }
        if (this.state.isOpen === false && prevState.isOpen) {
            document.removeEventListener('click', this.handleClickOutside, true);
        }
    }
    componentWillUnmount() {
        document.removeEventListener('click', this.handleClickOutside, true);
        this.portalEl.remove();
    }
    generateSortLink(field) {
        const { eventView, tableMeta, location } = this.props;
        if (!tableMeta) {
            return undefined;
        }
        const nextEventView = eventView.sortOnField(field, tableMeta, 'desc');
        const queryStringObject = nextEventView.generateQueryStringObject();
        return Object.assign(Object.assign({}, location), { query: Object.assign(Object.assign({}, location.query), { sort: queryStringObject.sort }) });
    }
    renderMenuItem(operation, title) {
        const { eventView } = this.props;
        return (<DropdownMenuItem>
        <MenuItemContent>
          <RadioLabel>
            <StyledRadio readOnly radioSize="small" checked={eventView.sorts.some(({ field }) => field === operation)} onClick={() => {
                const sortLink = this.generateSortLink({ field: operation });
                if (sortLink)
                    react_router_1.browserHistory.push(sortLink);
            }}/>
            <span>{title}</span>
          </RadioLabel>
        </MenuItemContent>
      </DropdownMenuItem>);
    }
    renderMenuContent() {
        return (<DropdownContent>
        {this.renderMenuItem('spans.http', (0, locale_1.t)('Sort By HTTP'))}
        {this.renderMenuItem('spans.db', (0, locale_1.t)('Sort By DB'))}
        {this.renderMenuItem('spans.resource', (0, locale_1.t)('Sort By Resource'))}
        {this.renderMenuItem('spans.browser', (0, locale_1.t)('Sort By Browser'))}
      </DropdownContent>);
    }
    renderMenu() {
        const modifiers = {
            hide: {
                enabled: false,
            },
            preventOverflow: {
                padding: 10,
                enabled: true,
                boundariesElement: 'viewport',
            },
        };
        return react_dom_1.default.createPortal(<react_popper_1.Popper placement="top" modifiers={modifiers}>
        {({ ref: popperRef, style, placement }) => (<DropdownWrapper ref={ref => {
                    popperRef(ref);
                    this.menuEl = ref;
                }} style={style} data-placement={placement}>
            {this.renderMenuContent()}
          </DropdownWrapper>)}
      </react_popper_1.Popper>, this.portalEl);
    }
    render() {
        const { title: Title } = this.props;
        const { isOpen } = this.state;
        const menu = isOpen ? this.renderMenu() : null;
        return (<react_popper_1.Manager>
        <react_popper_1.Reference>
          {({ ref }) => (<TitleWrapper ref={ref}>
              <Title onClick={this.toggleOpen}/>
            </TitleWrapper>)}
        </react_popper_1.Reference>
        {menu}
      </react_popper_1.Manager>);
    }
}
const DropdownWrapper = (0, styled_1.default)('div') `
  /* Adapted from the dropdown-menu class */
  border: none;
  border-radius: 2px;
  box-shadow: 0 0 0 1px rgba(52, 60, 69, 0.2), 0 1px 3px rgba(70, 82, 98, 0.25);
  background-clip: padding-box;
  background-color: ${p => p.theme.background};
  width: 220px;
  overflow: visible;
  z-index: ${p => p.theme.zIndex.tooltip};

  &:before,
  &:after {
    width: 0;
    height: 0;
    content: '';
    display: block;
    position: absolute;
    right: auto;
  }

  &:before {
    border-left: 9px solid transparent;
    border-right: 9px solid transparent;
    left: calc(50% - 9px);
    z-index: -2;
  }

  &:after {
    border-left: 8px solid transparent;
    border-right: 8px solid transparent;
    left: calc(50% - 8px);
    z-index: -1;
  }

  &[data-placement*='bottom'] {
    margin-top: 9px;

    &:before {
      border-bottom: 9px solid ${p => p.theme.border};
      top: -9px;
    }

    &:after {
      border-bottom: 8px solid ${p => p.theme.background};
      top: -8px;
    }
  }

  &[data-placement*='top'] {
    margin-bottom: 9px;

    &:before {
      border-top: 9px solid ${p => p.theme.border};
      bottom: -9px;
    }

    &:after {
      border-top: 8px solid ${p => p.theme.background};
      bottom: -8px;
    }
  }
`;
const DropdownMenuItem = (0, styled_1.default)(menuItem_1.default) `
  font-size: ${p => p.theme.fontSizeMedium};

  &:not(:last-child) {
    border-bottom: 1px solid ${p => p.theme.innerBorder};
  }
`;
const MenuItemContent = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  width: 100%;
`;
const RadioLabel = (0, styled_1.default)('label') `
  display: grid;
  cursor: pointer;
  grid-gap: 0.25em 0.5em;
  grid-template-columns: max-content auto;
  align-items: center;
  outline: none;
  font-weight: normal;
  margin: 0;
`;
const StyledRadio = (0, styled_1.default)(radio_1.default) `
  margin: 0;
`;
const DropdownContent = (0, styled_1.default)('div') `
  max-height: 250px;
  overflow-y: auto;
`;
const TitleWrapper = (0, styled_1.default)('div') `
  cursor: pointer;
`;
exports.default = OperationSort;
//# sourceMappingURL=operationSort.jsx.map