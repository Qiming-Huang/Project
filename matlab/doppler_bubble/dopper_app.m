classdef dopper_app < matlab.apps.AppBase

    % Properties that correspond to app components
    properties (Access = public)
        UIFigure             matlab.ui.Figure
        UIAxes               matlab.ui.control.UIAxes
        ImageEditFieldLabel  matlab.ui.control.Label
        ImageEditField       matlab.ui.control.NumericEditField
        TotalEditFieldLabel  matlab.ui.control.Label
        TotalEditField       matlab.ui.control.NumericEditField
        HelpButton           matlab.ui.control.StateButton
        ChoosefolderButton   matlab.ui.control.Button
        PreviousButton       matlab.ui.control.Button
        NextButton           matlab.ui.control.Button
        FButton              matlab.ui.control.Button
        SCTZRButton          matlab.ui.control.Button
        STEButton            matlab.ui.control.Button
    end

    
    properties (Access = private)
        x   % time domain y
        Fs  
        ts  % time domain x
        f   % frequency domain x
        P1  % frequency domain y
        zc  % zc(out) is STZCR's y
        t   % STZCR/STE x
        E   % E(out) is STE's y
        out
        % ........
        filePath  %
        fileList
        maxInd
        currentInd
        fix
    end
    
    methods (Access = private)
        
        function zc = zerocross(app, x, wintype, winamp, winlen)
%             error(nargchk(1,4,nargin,'struct'));
            x1 = x;
            x2 = [0, x(1:end-1)];
            
            % generate the first difference
            firstDiff = sgn(app,x1) - sgn(app,x2);
            
            % magnitude only
            absFirstDiff = abs(firstDiff);
            
            % lowpass filtering with window
            zc = winconv(app,absFirstDiff,wintype,winamp,winlen);
        end
        
        function En = energy(app, x , wintype, winamp, winlen)
%             error(nargchk(1,4,nargin,'struct'));
            
            % generate the window
            win = (winamp*(window(str2func(wintype),winlen))).';
            
            % enery calculation
            x2 = x.^2;
            En = winconv(app,x2,wintype,win,winlen);            
        end
        
        function y = winconv(app, x, varargin)
%             error(nargchk(1,4,nargin,'struct'));
            
            len = length(varargin);
            switch len
                case 0
                    wintype = 'rectwin';
                    A = 1;
                    L = length(x);
                case 1
                    if ischar(varargin{1})
                        wintype = lower(varargin{1});
                        A = 1;
                        L = length(x);
                    end
                case 2
                    if ischar(varargin{1}) && isreal(varargin{2})
                        wintype = lower(varargin{1});
                        A = varargin{2};
                        L = length(x);
                    end
                case 3
                    if ischar(varargin{1}) && isreal(varargin{2}) &&...
                            isreal(varargin{3})
                        wintype = lower(varargin{1});
                        A = varargin{2};
                        L = varargin{3};
                    end
            end
            
            % generate the window
            w1 = (window(str2func(wintype),L)).'; A = A(:).';
            w = A.*w1;
            
            % perform the convolution using FFT
            NFFT = 2^(nextpow2(length(x)+L));
            X = fft(x,NFFT); W = fft(w,NFFT);
            Y = X.*W;
            y = ifft(Y,NFFT);            
        end
        
        function y = sgn(app, x)
            y = (x>=0) + (-1)*(x<0);
        end        
        
        function update(app)
            [app.x,app.Fs] = audioread(app.fileList(app.currentInd).name);
            app.x = app.x.';
            
            app.x = (app.x(1,:) + app.x(2,:));
            
            N = length(app.x); % signal length
            n = 0:N-1;
            app.ts = n*(1/app.Fs); % time for signal
            
            L = length(app.x);
            app.f = app.Fs*(0:(L/2))/L;
            x_ = fft(app.x);
            P2 = abs(x_/L);
            app.P1 = L*P2(1:L/2+1); 
            app.P1(2:end-1) = 2*app.P1(2:end-1);
            
            % define the window
            wintype = 'rectwin';
            winlen = 201;
            winamp = [0.5,1]*(1/winlen);
            
            % find the zero-crossing rate
            app.zc = zerocross(app,app.x,wintype,winamp(1),winlen);
            
            % find the zero-crossing rate
            app.E = energy(app,app.x,wintype,winamp(2),winlen);
            
            % time index for the ST-ZCR and STE after delay compensation
            app.out = (winlen-1)/2:(N+winlen-1)-(winlen-1)/2;
            app.t = (app.out-(winlen-1)/2)*(1/app.Fs);
        end
    end


    % Callbacks that handle component events
    methods (Access = private)

        % Code that executes after component creation
        function startupFcn(app)
            
        end

        % Button pushed function: FButton
        function FButtonPushed(app, event)
            hold(app.UIAxes, "off");
            app.update();
            app.fix = 1;
            plot(app.UIAxes,app.f, app.P1)
            app.UIAxes.XLim = [0 2000];
        end

        % Button pushed function: SCTZRButton
        function SCTZRButtonPushed(app, event)
            hold(app.UIAxes, "off");
            app.fix = 2;             
            plot(app.UIAxes, app.ts, app.x);
            app.UIAxes.XLim = [-inf inf];
            plot(app.UIAxes, app.ts, app.x); 
            hold(app.UIAxes, "on");
            plot(app.UIAxes,app.t,app.zc(app.out),'r','Linewidth',2); 
            xlabel(app.UIAxes, 't, seconds');
            title(app.UIAxes, 'Short-time Zero Crossing Rate');
            legend(app.UIAxes, 'signal','STZCR');
        end

        % Button pushed function: STEButton
        function STEButtonPushed(app, event)
            hold(app.UIAxes, "off");
            app.fix = 3; 
            plot(app.UIAxes, app.ts,app.x);
            app.UIAxes.XLim = [-inf inf];
            hold(app.UIAxes, "on");
            plot(app.UIAxes, app.t,app.E(app.out),'r','Linewidth',2); 
            xlabel(app.UIAxes,'t, seconds');
            title(app.UIAxes, 'Short-time Energy');
            legend(app.UIAxes,'signal','STE');      
        end

        % Button pushed function: NextButton
        function NextButtonPushed(app, event)
            hold(app.UIAxes, "off");
            if app.currentInd == app.maxInd
                msgbox("This is the end")
            elseif app.fix == 1
                app.FButtonPushed();
            elseif app.fix == 2
                app.SCTZRButtonPushed();
            elseif app.fix == 3
                app.STEButtonPushed();
            end
            app.update();
            if app.currentInd <= app.maxInd
                app.currentInd = app.currentInd + 1;
            end
            app.ImageEditField.Value = app.currentInd;
        end

        % Button pushed function: ChoosefolderButton
        function ChoosefolderButtonPushed(app, event)
            app.filePath = uigetdir;
            cd(app.filePath);
            app.fileList = dir("*wav");
            app.maxInd = length(app.fileList);
            app.TotalEditField.Value = app.maxInd;
            app.ImageEditField.Value = 1;
            app.currentInd = 1;
            app.fix = 1;
            msgbox("Images loaded!");
        end

        % Button pushed function: PreviousButton
        function PreviousButtonPushed(app, event)
            hold(app.UIAxes, "off");
            if app.currentInd == 1
                msgbox("This is the first image")
            elseif app.fix == 1
                app.FButtonPushed();
            elseif app.fix == 2
                app.SCTZRButtonPushed();
            elseif app.fix == 3
                app.STEButtonPushed();
            end
            app.update();
            if app.currentInd >= 2
                app.currentInd = app.currentInd - 1;
            end
            app.ImageEditField.Value = app.currentInd;
        end
    end

    % Component initialization
    methods (Access = private)

        % Create UIFigure and components
        function createComponents(app)

            % Create UIFigure and hide until all components are created
            app.UIFigure = uifigure('Visible', 'off');
            app.UIFigure.Position = [100 100 886 658];
            app.UIFigure.Name = 'UI Figure';

            % Create UIAxes
            app.UIAxes = uiaxes(app.UIFigure);
            title(app.UIAxes, 'Title')
            xlabel(app.UIAxes, 'X')
            ylabel(app.UIAxes, 'Y')
            app.UIAxes.Position = [22 97 827 467];

            % Create ImageEditFieldLabel
            app.ImageEditFieldLabel = uilabel(app.UIFigure);
            app.ImageEditFieldLabel.HorizontalAlignment = 'right';
            app.ImageEditFieldLabel.Position = [50 623 39 22];
            app.ImageEditFieldLabel.Text = 'Image';

            % Create ImageEditField
            app.ImageEditField = uieditfield(app.UIFigure, 'numeric');
            app.ImageEditField.Position = [104 623 26 22];

            % Create TotalEditFieldLabel
            app.TotalEditFieldLabel = uilabel(app.UIFigure);
            app.TotalEditFieldLabel.HorizontalAlignment = 'right';
            app.TotalEditFieldLabel.Position = [50 587 31 22];
            app.TotalEditFieldLabel.Text = 'Total';

            % Create TotalEditField
            app.TotalEditField = uieditfield(app.UIFigure, 'numeric');
            app.TotalEditField.Position = [106 587 22 22];

            % Create HelpButton
            app.HelpButton = uibutton(app.UIFigure, 'state');
            app.HelpButton.Text = 'Help';
            app.HelpButton.BackgroundColor = [1 0.4118 0.1608];
            app.HelpButton.Position = [684 602 100 22];

            % Create ChoosefolderButton
            app.ChoosefolderButton = uibutton(app.UIFigure, 'push');
            app.ChoosefolderButton.ButtonPushedFcn = createCallbackFcn(app, @ChoosefolderButtonPushed, true);
            app.ChoosefolderButton.BackgroundColor = [0.651 0.651 0.651];
            app.ChoosefolderButton.Position = [148 48 100 22];
            app.ChoosefolderButton.Text = 'Choose folder';

            % Create PreviousButton
            app.PreviousButton = uibutton(app.UIFigure, 'push');
            app.PreviousButton.ButtonPushedFcn = createCallbackFcn(app, @PreviousButtonPushed, true);
            app.PreviousButton.BackgroundColor = [0.8 0.8 0.8];
            app.PreviousButton.Position = [362 48 100 22];
            app.PreviousButton.Text = 'Previous';

            % Create NextButton
            app.NextButton = uibutton(app.UIFigure, 'push');
            app.NextButton.ButtonPushedFcn = createCallbackFcn(app, @NextButtonPushed, true);
            app.NextButton.BackgroundColor = [0.8 0.8 0.8];
            app.NextButton.Position = [599 48 100 22];
            app.NextButton.Text = 'Next';

            % Create FButton
            app.FButton = uibutton(app.UIFigure, 'push');
            app.FButton.ButtonPushedFcn = createCallbackFcn(app, @FButtonPushed, true);
            app.FButton.BackgroundColor = [0.0745 0.6235 1];
            app.FButton.Position = [184 602 100 22];
            app.FButton.Text = 'F';

            % Create SCTZRButton
            app.SCTZRButton = uibutton(app.UIFigure, 'push');
            app.SCTZRButton.ButtonPushedFcn = createCallbackFcn(app, @SCTZRButtonPushed, true);
            app.SCTZRButton.BackgroundColor = [0.0745 0.6235 1];
            app.SCTZRButton.Position = [353 602 100 22];
            app.SCTZRButton.Text = 'SCTZR';

            % Create STEButton
            app.STEButton = uibutton(app.UIFigure, 'push');
            app.STEButton.ButtonPushedFcn = createCallbackFcn(app, @STEButtonPushed, true);
            app.STEButton.BackgroundColor = [0.0745 0.6235 1];
            app.STEButton.Position = [524 602 100 22];
            app.STEButton.Text = 'STE';

            % Show the figure after all components are created
            app.UIFigure.Visible = 'on';
        end
    end

    % App creation and deletion
    methods (Access = public)

        % Construct app
        function app = dopper_app

            % Create UIFigure and components
            createComponents(app)

            % Register the app with App Designer
            registerApp(app, app.UIFigure)

            % Execute the startup function
            runStartupFcn(app, @startupFcn)

            if nargout == 0
                clear app
            end
        end

        % Code that executes before app deletion
        function delete(app)

            % Delete UIFigure when app is deleted
            delete(app.UIFigure)
        end
    end
end