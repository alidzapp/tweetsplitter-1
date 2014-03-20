var tweetSplitter = angular.module('tweetSplitter', []);

var tweetSplitter = tweetSplitter.config(function($httpProvider, $interpolateProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

function postController($scope, $http) {
    $scope.postUrl = '/post_ajax';
    $scope.formData = {}
    $scope.postTweet = function() {
        var requestForm = $http({method: 'POST',
                               url: $scope.postUrl,
                               data: $scope.formData
        }).success(function(data) {
            if (data.success) {
                $scope.success = data.message;
            } else {
                $scope.error = data.message;
            }
        })

    }
}