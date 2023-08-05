/*! For license information please see 1170f23f.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[59799],{45253:(t,i,e)=>{e.d(i,{UX:()=>s,j2:()=>r,KT:()=>a,HX:()=>o,Ns:()=>n});var o,n,s={ANCHOR:"mdc-menu-surface--anchor",ANIMATING_CLOSED:"mdc-menu-surface--animating-closed",ANIMATING_OPEN:"mdc-menu-surface--animating-open",FIXED:"mdc-menu-surface--fixed",IS_OPEN_BELOW:"mdc-menu-surface--is-open-below",OPEN:"mdc-menu-surface--open",ROOT:"mdc-menu-surface"},r={CLOSED_EVENT:"MDCMenuSurface:closed",CLOSING_EVENT:"MDCMenuSurface:closing",OPENED_EVENT:"MDCMenuSurface:opened",FOCUSABLE_ELEMENTS:["button:not(:disabled)",'[href]:not([aria-disabled="true"])',"input:not(:disabled)","select:not(:disabled)","textarea:not(:disabled)",'[tabindex]:not([tabindex="-1"]):not([aria-disabled="true"])'].join(", ")},a={TRANSITION_OPEN_DURATION:120,TRANSITION_CLOSE_DURATION:75,MARGIN_TO_EDGE:32,ANCHOR_TO_MENU_SURFACE_WIDTH_RATIO:.67,TOUCH_EVENT_WAIT_MS:30};!function(t){t[t.BOTTOM=1]="BOTTOM",t[t.CENTER=2]="CENTER",t[t.RIGHT=4]="RIGHT",t[t.FLIP_RTL=8]="FLIP_RTL"}(o||(o={})),function(t){t[t.TOP_LEFT=0]="TOP_LEFT",t[t.TOP_RIGHT=4]="TOP_RIGHT",t[t.BOTTOM_LEFT=1]="BOTTOM_LEFT",t[t.BOTTOM_RIGHT=5]="BOTTOM_RIGHT",t[t.TOP_START=8]="TOP_START",t[t.TOP_END=12]="TOP_END",t[t.BOTTOM_START=9]="BOTTOM_START",t[t.BOTTOM_END=13]="BOTTOM_END"}(n||(n={}))},6945:(t,i,e)=>{e.d(i,{k:()=>r,Z:()=>a});var o=e(87480),n=e(72774),s=e(45253),r=function(t){function i(e){var n=t.call(this,(0,o.__assign)((0,o.__assign)({},i.defaultAdapter),e))||this;return n.isSurfaceOpen=!1,n.isQuickOpen=!1,n.isHoistedElement=!1,n.isFixedPosition=!1,n.isHorizontallyCenteredOnViewport=!1,n.maxHeight=0,n.openAnimationEndTimerId=0,n.closeAnimationEndTimerId=0,n.animationRequestId=0,n.anchorCorner=s.Ns.TOP_START,n.originCorner=s.Ns.TOP_START,n.anchorMargin={top:0,right:0,bottom:0,left:0},n.position={x:0,y:0},n}return(0,o.__extends)(i,t),Object.defineProperty(i,"cssClasses",{get:function(){return s.UX},enumerable:!1,configurable:!0}),Object.defineProperty(i,"strings",{get:function(){return s.j2},enumerable:!1,configurable:!0}),Object.defineProperty(i,"numbers",{get:function(){return s.KT},enumerable:!1,configurable:!0}),Object.defineProperty(i,"Corner",{get:function(){return s.Ns},enumerable:!1,configurable:!0}),Object.defineProperty(i,"defaultAdapter",{get:function(){return{addClass:function(){},removeClass:function(){},hasClass:function(){return!1},hasAnchor:function(){return!1},isElementInContainer:function(){return!1},isFocused:function(){return!1},isRtl:function(){return!1},getInnerDimensions:function(){return{height:0,width:0}},getAnchorDimensions:function(){return null},getWindowDimensions:function(){return{height:0,width:0}},getBodyDimensions:function(){return{height:0,width:0}},getWindowScroll:function(){return{x:0,y:0}},setPosition:function(){},setMaxHeight:function(){},setTransformOrigin:function(){},saveFocus:function(){},restoreFocus:function(){},notifyClose:function(){},notifyOpen:function(){},notifyClosing:function(){}}},enumerable:!1,configurable:!0}),i.prototype.init=function(){var t=i.cssClasses,e=t.ROOT,o=t.OPEN;if(!this.adapter.hasClass(e))throw new Error(e+" class required in root element.");this.adapter.hasClass(o)&&(this.isSurfaceOpen=!0)},i.prototype.destroy=function(){clearTimeout(this.openAnimationEndTimerId),clearTimeout(this.closeAnimationEndTimerId),cancelAnimationFrame(this.animationRequestId)},i.prototype.setAnchorCorner=function(t){this.anchorCorner=t},i.prototype.flipCornerHorizontally=function(){this.originCorner=this.originCorner^s.HX.RIGHT},i.prototype.setAnchorMargin=function(t){this.anchorMargin.top=t.top||0,this.anchorMargin.right=t.right||0,this.anchorMargin.bottom=t.bottom||0,this.anchorMargin.left=t.left||0},i.prototype.setIsHoisted=function(t){this.isHoistedElement=t},i.prototype.setFixedPosition=function(t){this.isFixedPosition=t},i.prototype.isFixed=function(){return this.isFixedPosition},i.prototype.setAbsolutePosition=function(t,i){this.position.x=this.isFinite(t)?t:0,this.position.y=this.isFinite(i)?i:0},i.prototype.setIsHorizontallyCenteredOnViewport=function(t){this.isHorizontallyCenteredOnViewport=t},i.prototype.setQuickOpen=function(t){this.isQuickOpen=t},i.prototype.setMaxHeight=function(t){this.maxHeight=t},i.prototype.isOpen=function(){return this.isSurfaceOpen},i.prototype.open=function(){var t=this;this.isSurfaceOpen||(this.adapter.saveFocus(),this.isQuickOpen?(this.isSurfaceOpen=!0,this.adapter.addClass(i.cssClasses.OPEN),this.dimensions=this.adapter.getInnerDimensions(),this.autoposition(),this.adapter.notifyOpen()):(this.adapter.addClass(i.cssClasses.ANIMATING_OPEN),this.animationRequestId=requestAnimationFrame((function(){t.dimensions=t.adapter.getInnerDimensions(),t.autoposition(),t.adapter.addClass(i.cssClasses.OPEN),t.openAnimationEndTimerId=setTimeout((function(){t.openAnimationEndTimerId=0,t.adapter.removeClass(i.cssClasses.ANIMATING_OPEN),t.adapter.notifyOpen()}),s.KT.TRANSITION_OPEN_DURATION)})),this.isSurfaceOpen=!0))},i.prototype.close=function(t){var e=this;if(void 0===t&&(t=!1),this.isSurfaceOpen){if(this.adapter.notifyClosing(),this.isQuickOpen)return this.isSurfaceOpen=!1,t||this.maybeRestoreFocus(),this.adapter.removeClass(i.cssClasses.OPEN),this.adapter.removeClass(i.cssClasses.IS_OPEN_BELOW),void this.adapter.notifyClose();this.adapter.addClass(i.cssClasses.ANIMATING_CLOSED),requestAnimationFrame((function(){e.adapter.removeClass(i.cssClasses.OPEN),e.adapter.removeClass(i.cssClasses.IS_OPEN_BELOW),e.closeAnimationEndTimerId=setTimeout((function(){e.closeAnimationEndTimerId=0,e.adapter.removeClass(i.cssClasses.ANIMATING_CLOSED),e.adapter.notifyClose()}),s.KT.TRANSITION_CLOSE_DURATION)})),this.isSurfaceOpen=!1,t||this.maybeRestoreFocus()}},i.prototype.handleBodyClick=function(t){var i=t.target;this.adapter.isElementInContainer(i)||this.close()},i.prototype.handleKeydown=function(t){var i=t.keyCode;("Escape"===t.key||27===i)&&this.close()},i.prototype.autoposition=function(){var t;this.measurements=this.getAutoLayoutmeasurements();var e=this.getoriginCorner(),o=this.getMenuSurfaceMaxHeight(e),n=this.hasBit(e,s.HX.BOTTOM)?"bottom":"top",r=this.hasBit(e,s.HX.RIGHT)?"right":"left",a=this.getHorizontalOriginOffset(e),h=this.getVerticalOriginOffset(e),c=this.measurements,d=c.anchorSize,u=c.surfaceSize,p=((t={})[r]=a,t[n]=h,t);d.width/u.width>s.KT.ANCHOR_TO_MENU_SURFACE_WIDTH_RATIO&&(r="center"),(this.isHoistedElement||this.isFixedPosition)&&this.adjustPositionForHoistedElement(p),this.adapter.setTransformOrigin(r+" "+n),this.adapter.setPosition(p),this.adapter.setMaxHeight(o?o+"px":""),this.hasBit(e,s.HX.BOTTOM)||this.adapter.addClass(i.cssClasses.IS_OPEN_BELOW)},i.prototype.getAutoLayoutmeasurements=function(){var t=this.adapter.getAnchorDimensions(),i=this.adapter.getBodyDimensions(),e=this.adapter.getWindowDimensions(),o=this.adapter.getWindowScroll();return t||(t={top:this.position.y,right:this.position.x,bottom:this.position.y,left:this.position.x,width:0,height:0}),{anchorSize:t,bodySize:i,surfaceSize:this.dimensions,viewportDistance:{top:t.top,right:e.width-t.right,bottom:e.height-t.bottom,left:t.left},viewportSize:e,windowScroll:o}},i.prototype.getoriginCorner=function(){var t,e,o=this.originCorner,n=this.measurements,r=n.viewportDistance,a=n.anchorSize,h=n.surfaceSize,c=i.numbers.MARGIN_TO_EDGE;this.hasBit(this.anchorCorner,s.HX.BOTTOM)?(t=r.top-c+this.anchorMargin.bottom,e=r.bottom-c-this.anchorMargin.bottom):(t=r.top-c+this.anchorMargin.top,e=r.bottom-c+a.height-this.anchorMargin.top),!(e-h.height>0)&&t>e&&(o=this.setBit(o,s.HX.BOTTOM));var d,u,p=this.adapter.isRtl(),l=this.hasBit(this.anchorCorner,s.HX.FLIP_RTL),m=this.hasBit(this.anchorCorner,s.HX.RIGHT)||this.hasBit(o,s.HX.RIGHT),f=!1;(f=p&&l?!m:m)?(d=r.left+a.width+this.anchorMargin.right,u=r.right-this.anchorMargin.right):(d=r.left+this.anchorMargin.left,u=r.right+a.width-this.anchorMargin.left);var T=d-h.width>0,g=u-h.width>0,y=this.hasBit(o,s.HX.FLIP_RTL)&&this.hasBit(o,s.HX.RIGHT);return g&&y&&p||!T&&y?o=this.unsetBit(o,s.HX.RIGHT):(T&&f&&p||T&&!f&&m||!g&&d>=u)&&(o=this.setBit(o,s.HX.RIGHT)),o},i.prototype.getMenuSurfaceMaxHeight=function(t){if(this.maxHeight>0)return this.maxHeight;var e=this.measurements.viewportDistance,o=0,n=this.hasBit(t,s.HX.BOTTOM),r=this.hasBit(this.anchorCorner,s.HX.BOTTOM),a=i.numbers.MARGIN_TO_EDGE;return n?(o=e.top+this.anchorMargin.top-a,r||(o+=this.measurements.anchorSize.height)):(o=e.bottom-this.anchorMargin.bottom+this.measurements.anchorSize.height-a,r&&(o-=this.measurements.anchorSize.height)),o},i.prototype.getHorizontalOriginOffset=function(t){var i=this.measurements.anchorSize,e=this.hasBit(t,s.HX.RIGHT),o=this.hasBit(this.anchorCorner,s.HX.RIGHT);if(e){var n=o?i.width-this.anchorMargin.left:this.anchorMargin.right;return this.isHoistedElement||this.isFixedPosition?n-(this.measurements.viewportSize.width-this.measurements.bodySize.width):n}return o?i.width-this.anchorMargin.right:this.anchorMargin.left},i.prototype.getVerticalOriginOffset=function(t){var i=this.measurements.anchorSize,e=this.hasBit(t,s.HX.BOTTOM),o=this.hasBit(this.anchorCorner,s.HX.BOTTOM);return e?o?i.height-this.anchorMargin.top:-this.anchorMargin.bottom:o?i.height+this.anchorMargin.bottom:this.anchorMargin.top},i.prototype.adjustPositionForHoistedElement=function(t){var i,e,n=this.measurements,s=n.windowScroll,r=n.viewportDistance,a=n.surfaceSize,h=n.viewportSize,c=Object.keys(t);try{for(var d=(0,o.__values)(c),u=d.next();!u.done;u=d.next()){var p=u.value,l=t[p]||0;!this.isHorizontallyCenteredOnViewport||"left"!==p&&"right"!==p?(l+=r[p],this.isFixedPosition||("top"===p?l+=s.y:"bottom"===p?l-=s.y:"left"===p?l+=s.x:l-=s.x),t[p]=l):t[p]=(h.width-a.width)/2}}catch(t){i={error:t}}finally{try{u&&!u.done&&(e=d.return)&&e.call(d)}finally{if(i)throw i.error}}},i.prototype.maybeRestoreFocus=function(){var t=this,i=this.adapter.isFocused(),e=document.activeElement&&this.adapter.isElementInContainer(document.activeElement);(i||e)&&setTimeout((function(){t.adapter.restoreFocus()}),s.KT.TOUCH_EVENT_WAIT_MS)},i.prototype.hasBit=function(t,i){return Boolean(t&i)},i.prototype.setBit=function(t,i){return t|i},i.prototype.unsetBit=function(t,i){return t^i},i.prototype.isFinite=function(t){return"number"==typeof t&&isFinite(t)},i}(n.K);const a=r},59799:(t,i,e)=>{var o=e(87480),n=e(32207),s=e(45253),r=e(6945),a=e(78220),h=e(14114),c=e(82612),d=e(59685),u=e(84298);const p={TOP_LEFT:s.Ns.TOP_LEFT,TOP_RIGHT:s.Ns.TOP_RIGHT,BOTTOM_LEFT:s.Ns.BOTTOM_LEFT,BOTTOM_RIGHT:s.Ns.BOTTOM_RIGHT,TOP_START:s.Ns.TOP_START,TOP_END:s.Ns.TOP_END,BOTTOM_START:s.Ns.BOTTOM_START,BOTTOM_END:s.Ns.BOTTOM_END};class l extends a.H{constructor(){super(...arguments),this.mdcFoundationClass=r.Z,this.absolute=!1,this.fullwidth=!1,this.fixed=!1,this.x=null,this.y=null,this.quick=!1,this.open=!1,this.stayOpenOnBodyClick=!1,this.bitwiseCorner=s.Ns.TOP_START,this.previousMenuCorner=null,this.menuCorner="START",this.corner="TOP_START",this.styleTop="",this.styleLeft="",this.styleRight="",this.styleBottom="",this.styleMaxHeight="",this.styleTransformOrigin="",this.anchor=null,this.previouslyFocused=null,this.previousAnchor=null,this.onBodyClickBound=()=>{}}render(){const t={"mdc-menu-surface--fixed":this.fixed,"mdc-menu-surface--fullwidth":this.fullwidth},i={top:this.styleTop,left:this.styleLeft,right:this.styleRight,bottom:this.styleBottom,"max-height":this.styleMaxHeight,"transform-origin":this.styleTransformOrigin};return n.dy`
      <div
          class="mdc-menu-surface ${(0,d.$)(t)}"
          style="${(0,u.V)(i)}"
          @keydown=${this.onKeydown}
          @opened=${this.registerBodyClick}
          @closed=${this.deregisterBodyClick}>
        <slot></slot>
      </div>`}createAdapter(){return Object.assign(Object.assign({},(0,a.q)(this.mdcRoot)),{hasAnchor:()=>!!this.anchor,notifyClose:()=>{const t=new CustomEvent("closed",{bubbles:!0,composed:!0});this.open=!1,this.mdcRoot.dispatchEvent(t)},notifyClosing:()=>{const t=new CustomEvent("closing",{bubbles:!0,composed:!0});this.mdcRoot.dispatchEvent(t)},notifyOpen:()=>{const t=new CustomEvent("opened",{bubbles:!0,composed:!0});this.open=!0,this.mdcRoot.dispatchEvent(t)},isElementInContainer:()=>!1,isRtl:()=>!!this.mdcRoot&&"rtl"===getComputedStyle(this.mdcRoot).direction,setTransformOrigin:t=>{this.mdcRoot&&(this.styleTransformOrigin=t)},isFocused:()=>(0,c.WU)(this),saveFocus:()=>{const t=(0,c.Mh)(),i=t.length;i||(this.previouslyFocused=null),this.previouslyFocused=t[i-1]},restoreFocus:()=>{this.previouslyFocused&&"focus"in this.previouslyFocused&&this.previouslyFocused.focus()},getInnerDimensions:()=>{const t=this.mdcRoot;return t?{width:t.offsetWidth,height:t.offsetHeight}:{width:0,height:0}},getAnchorDimensions:()=>{const t=this.anchor;return t?t.getBoundingClientRect():null},getBodyDimensions:()=>({width:document.body.clientWidth,height:document.body.clientHeight}),getWindowDimensions:()=>({width:window.innerWidth,height:window.innerHeight}),getWindowScroll:()=>({x:window.pageXOffset,y:window.pageYOffset}),setPosition:t=>{this.mdcRoot&&(this.styleLeft="left"in t?`${t.left}px`:"",this.styleRight="right"in t?`${t.right}px`:"",this.styleTop="top"in t?`${t.top}px`:"",this.styleBottom="bottom"in t?`${t.bottom}px`:"")},setMaxHeight:async t=>{this.mdcRoot&&(this.styleMaxHeight=t,await this.updateComplete,this.styleMaxHeight=`var(--mdc-menu-max-height, ${t})`)}})}onKeydown(t){this.mdcFoundation&&this.mdcFoundation.handleKeydown(t)}onBodyClick(t){if(this.stayOpenOnBodyClick)return;-1===t.composedPath().indexOf(this)&&this.close()}registerBodyClick(){this.onBodyClickBound=this.onBodyClick.bind(this),document.body.addEventListener("click",this.onBodyClickBound,{passive:!0,capture:!0})}deregisterBodyClick(){document.body.removeEventListener("click",this.onBodyClickBound,{capture:!0})}close(){this.open=!1}show(){this.open=!0}}(0,o.__decorate)([(0,n.IO)(".mdc-menu-surface")],l.prototype,"mdcRoot",void 0),(0,o.__decorate)([(0,n.IO)("slot")],l.prototype,"slotElement",void 0),(0,o.__decorate)([(0,n.Cb)({type:Boolean}),(0,h.P)((function(t){this.mdcFoundation&&!this.fixed&&this.mdcFoundation.setIsHoisted(t)}))],l.prototype,"absolute",void 0),(0,o.__decorate)([(0,n.Cb)({type:Boolean})],l.prototype,"fullwidth",void 0),(0,o.__decorate)([(0,n.Cb)({type:Boolean}),(0,h.P)((function(t){this.mdcFoundation&&!this.absolute&&this.mdcFoundation.setFixedPosition(t)}))],l.prototype,"fixed",void 0),(0,o.__decorate)([(0,n.Cb)({type:Number}),(0,h.P)((function(t){this.mdcFoundation&&null!==this.y&&null!==t&&(this.mdcFoundation.setAbsolutePosition(t,this.y),this.mdcFoundation.setAnchorMargin({left:t,top:this.y,right:-t,bottom:this.y}))}))],l.prototype,"x",void 0),(0,o.__decorate)([(0,n.Cb)({type:Number}),(0,h.P)((function(t){this.mdcFoundation&&null!==this.x&&null!==t&&(this.mdcFoundation.setAbsolutePosition(this.x,t),this.mdcFoundation.setAnchorMargin({left:this.x,top:t,right:-this.x,bottom:t}))}))],l.prototype,"y",void 0),(0,o.__decorate)([(0,n.Cb)({type:Boolean}),(0,h.P)((function(t){this.mdcFoundation&&this.mdcFoundation.setQuickOpen(t)}))],l.prototype,"quick",void 0),(0,o.__decorate)([(0,n.Cb)({type:Boolean,reflect:!0}),(0,h.P)((function(t,i){this.mdcFoundation&&(t?this.mdcFoundation.open():void 0!==i&&this.mdcFoundation.close())}))],l.prototype,"open",void 0),(0,o.__decorate)([(0,n.Cb)({type:Boolean})],l.prototype,"stayOpenOnBodyClick",void 0),(0,o.__decorate)([(0,n.SB)(),(0,h.P)((function(t){this.mdcFoundation&&this.mdcFoundation.setAnchorCorner(t)}))],l.prototype,"bitwiseCorner",void 0),(0,o.__decorate)([(0,n.Cb)({type:String}),(0,h.P)((function(t){if(this.mdcFoundation){const i="START"===t||"END"===t,e=null===this.previousMenuCorner,o=!e&&t!==this.previousMenuCorner,n=e&&"END"===t;i&&(o||n)&&(this.bitwiseCorner=this.bitwiseCorner^s.HX.RIGHT,this.mdcFoundation.flipCornerHorizontally(),this.previousMenuCorner=t)}}))],l.prototype,"menuCorner",void 0),(0,o.__decorate)([(0,n.Cb)({type:String}),(0,h.P)((function(t){if(this.mdcFoundation&&t){let i=p[t];"END"===this.menuCorner&&(i^=s.HX.RIGHT),this.bitwiseCorner=i}}))],l.prototype,"corner",void 0),(0,o.__decorate)([(0,n.SB)()],l.prototype,"styleTop",void 0),(0,o.__decorate)([(0,n.SB)()],l.prototype,"styleLeft",void 0),(0,o.__decorate)([(0,n.SB)()],l.prototype,"styleRight",void 0),(0,o.__decorate)([(0,n.SB)()],l.prototype,"styleBottom",void 0),(0,o.__decorate)([(0,n.SB)()],l.prototype,"styleMaxHeight",void 0),(0,o.__decorate)([(0,n.SB)()],l.prototype,"styleTransformOrigin",void 0);const m=n.iv`.mdc-menu-surface{display:none;position:absolute;box-sizing:border-box;max-width:calc(100vw - 32px);max-width:var(--mdc-menu-max-width, calc(100vw - 32px));max-height:calc(100vh - 32px);max-height:var(--mdc-menu-max-height, calc(100vh - 32px));margin:0;padding:0;transform:scale(1);transform-origin:top left;opacity:0;overflow:auto;will-change:transform,opacity;z-index:8;transition:opacity .03s linear,transform .12s cubic-bezier(0, 0, 0.2, 1),height 250ms cubic-bezier(0, 0, 0.2, 1);box-shadow:0px 5px 5px -3px rgba(0, 0, 0, 0.2),0px 8px 10px 1px rgba(0, 0, 0, 0.14),0px 3px 14px 2px rgba(0,0,0,.12);background-color:#fff;background-color:var(--mdc-theme-surface, #fff);color:#000;color:var(--mdc-theme-on-surface, #000);border-radius:4px;border-radius:var(--mdc-shape-medium, 4px);transform-origin-left:top left;transform-origin-right:top right}.mdc-menu-surface:focus{outline:none}.mdc-menu-surface--animating-open{display:inline-block;transform:scale(0.8);opacity:0}.mdc-menu-surface--open{display:inline-block;transform:scale(1);opacity:1}.mdc-menu-surface--animating-closed{display:inline-block;opacity:0;transition:opacity .075s linear}[dir=rtl] .mdc-menu-surface,.mdc-menu-surface[dir=rtl]{transform-origin-left:top right;transform-origin-right:top left}.mdc-menu-surface--anchor{position:relative;overflow:visible}.mdc-menu-surface--fixed{position:fixed}.mdc-menu-surface--fullwidth{width:100%}:host(:not([open])){display:none}.mdc-menu-surface{z-index:8;z-index:var(--mdc-menu-z-index, 8);min-width:112px;min-width:var(--mdc-menu-min-width, 112px)}`;let f=class extends l{};f.styles=[m],f=(0,o.__decorate)([(0,n.Mo)("mwc-menu-surface")],f)}}]);
//# sourceMappingURL=1170f23f.js.map