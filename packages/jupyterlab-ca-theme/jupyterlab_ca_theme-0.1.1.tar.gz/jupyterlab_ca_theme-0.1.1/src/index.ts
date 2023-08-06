import {
  JupyterFrontEnd,
    JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IThemeManager } from '@jupyterlab/apputils';

import {
    IDisposable, DisposableDelegate
} from 'phosphor/lib/core/disposable';

import {
    Dialog,
    ISplashScreen
} from '@jupyterlab/apputils';

import '../style/index.css';

import { CommandRegistry } from 'phosphor/lib/ui/commandregistry';

namespace CommandIDs {
    export const changeTheme = 'apputils:change-theme';

    export const loadState = 'apputils:load-statedb';

    export const recoverState = 'apputils:recover-statedb';

    export const reset = 'apputils:reset';

    export const resetOnLoad = 'apputils:reset-on-load';

    export const saveState = 'apputils:save-statedb';
}


/**
 * Initialization data for the @composable/jupyterlab-ca-theme extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: '@composable/jupyterlab-ca-theme',
  requires: [IThemeManager],
  autoStart: true,
  activate: (app: JupyterFrontEnd, manager: IThemeManager) => {
    console.log('JupyterLab extension @composable/jupyterlab-ca-theme is activated!');
    const style = '@composable/jupyterlab-ca-theme/index.css';

    manager.register({
      name: '@composable/jupyterlab-ca-theme',
      isLight: true,
      load: () => manager.loadCSS(style),
      unload: () => Promise.resolve(undefined)
    });
  }
};

const splash: JupyterFrontEndPlugin<ISplashScreen> = {
    id: '@jupyterlab/mysplash:splash',
    autoStart: true,
    provides: ISplashScreen,
    activate: (app: any) => {
        return {
            show: (light = true) => {
                const { commands, restored } = app;

                return Private.showSplash(restored, commands, CommandIDs.reset, light);
            }
        };
    }
};

namespace Private {
    /**
     * Create a splash element.
     */
    function createSplash(): HTMLElement {
        const splash = document.createElement('div');
        const nyan = document.createElement('img');
        nyan.src = "https://media.giphy.com/media/3o85xBXz9cOahLB6w0/giphy.gif?cid=790b7611eb248b1d5aecf2fa118c1546f03e451affda2870&rid=giphy.gif&ct=g";
        nyan.classList.add('nyan');
        nyan.classList.add('animated');
        nyan.classList.add('bounce');
        splash.appendChild(nyan);
        splash.id = 'jupyterlab-splash';


        return splash;
    }

    /**
     * A debouncer for recovery attempts.
     */
    let debouncer = 0;

    /**
     * The recovery dialog.
     */
    let dialog: Dialog<any>;

    /**
     * Allows the user to clear state if splash screen takes too long.
     */
    function recover(fn: () => void): void {
        if (dialog) {
            return;
        }

        dialog = new Dialog({
            title: 'Loading...',
            body: `The loading screen is taking a long time.
        Would you like to clear the workspace or keep waiting?`,
            buttons: [
                Dialog.cancelButton({ label: 'Keep Waiting' }),
                Dialog.warnButton({ label: 'Clear Workspace' })
            ]
        });

        dialog
            .launch()
            .then(result => {
                if (result.button.accept) {
                    return fn();
                }

                dialog.dispose();
                dialog = null;

                debouncer = window.setTimeout(() => {
                    recover(fn);
                }, 700);
            })
            .catch(() => {
                /* no-op */
            });
    }

    /**
     * The splash element.
     */
    const splash = createSplash();

    /**
     * The splash screen counter.
     */
    let splashCount = 0;

    /**
     * Show the splash element.
     *
     * @param ready - A promise that must be resolved before splash disappears.
     *
     * @param recovery - A command that recovers from a hanging splash.
     */
    export function showSplash(
        ready: Promise<any>,
        commands: CommandRegistry,
        recovery: string,
        light: boolean
    ): IDisposable {
        splash.classList.remove('splash-fade');
        splash.classList.toggle('light', light);
        splash.classList.toggle('dark', !light);
        splashCount++;

        if (debouncer) {
            window.clearTimeout(debouncer);
        }
        debouncer = window.setTimeout(() => {
            if (commands.hasCommand(recovery)) {
                recover(() => {
                    commands.execute(recovery, {});
                });
            }
        }, 7000);

        document.body.appendChild(splash);

        return new DisposableDelegate(() => {
            ready.then(() => {
                if (--splashCount === 0) {
                    if (debouncer) {
                        window.clearTimeout(debouncer);
                        debouncer = 0;
                    }

                    if (dialog) {
                        dialog.dispose();
                        dialog = null;
                    }

                    splash.classList.add('splash-fade');
                    window.setTimeout(() => {
                        document.body.removeChild(splash);
                    }, 500);
                }
            });
        });
    }
}

const plugins: JupyterFrontEndPlugin<any>[] = [
    extension,
    splash
];
export default plugins;
