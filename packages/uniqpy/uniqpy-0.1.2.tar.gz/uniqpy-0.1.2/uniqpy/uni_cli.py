import argparse
import numpy as np
import warnings
warnings.filterwarnings('ignore')


from uniqpy.uniquac import fit_UNIQUAC_model, optimizeX




def main():


    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest='command')
    parser_fit = subparsers.add_parser('fit', help='fitting methods')
    parser_fit.add_argument('-l', '--l_table', type=str, required=True, help='table with liquid phase relative concentrations')
    parser_fit.add_argument('-v', '--v_table', type=str, required=True, help='table with vapour phase relative abundances')
    parser_fit.add_argument('-p', '--parameters', type=str, default='parameteres.txt', help='output')
    parser_fit.add_argument('-q', type=str, required=True, help='molecular surfaces')
    parser_fit.add_argument('-r', type=str, required=True, help='molecular volumes')
    

    parser_transform = subparsers.add_parser('transform', help='tranforming methods')
    parser_transform.add_argument('-v', '--v_table', type=str, help='table with vapour phase relative abundances')
    parser_transform.add_argument('-p', '--parameters', type=str, help='fitted parameters')
    parser_transform.add_argument('-o', '--output', type=str, default='liquid_data.txt', help='output')
    parser_transform.add_argument('-q', type=str, required=True, help='molecular surfaces')
    parser_transform.add_argument('-r', type=str, required=True, help='molecular volumes')

    args = parser.parse_args()



    for key in args.__dict__:
        print(key + ':', args.__dict__[key], sep='\t')

    print()
    R = np.loadtxt(args.r)
    Q = np.loadtxt(args.q)

    if args.command == 'fit':

        liquid_data = np.loadtxt(args.l_table)
        vapour_data = np.loadtxt(args.v_table)
        print('Model fitting...')
        best_parameters = fit_UNIQUAC_model(liquid_data, vapour_data, R, Q)

        np.savetxt(args.parameters, best_parameters)

        print('Model has been fitted! Paramteres were saved in {}'.format(args.parameters))


    if args.command == 'transform':

        vapour_data = np.loadtxt(args.v_table)
        model_paramteres = np.loadtxt(args.parameters)
        print('Liquid phase optimization...')

        pred_x = []

        sample = 1
        N = len(vapour_data)
        for y in vapour_data:
            print('\tSample {}'.format(sample), end='\r')
            pred_x.append(optimizeX(model_paramteres, y, R, Q))
            sample += 1
            print('\r', end='')
        print()

        pred_x = np.array(pred_x)

        np.savetxt(args.output, pred_x)
        print('done! Liquid phase concentrations were saved in {}'.format(args.output))
    
    
    

if __name__ == '__main__':
    main()
